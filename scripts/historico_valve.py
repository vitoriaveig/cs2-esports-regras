#!/usr/bin/env python3
"""Histórico das regras da Valve e base de exceções, a partir do histórico Git deste fork.

Este repositório é um fork de ValveSoftware/counter-strike_rules_and_regs, então o histórico dos arquivos
da Valve está aqui. O script:

1. exporta cada versão de cada arquivo da Valve para historico/valve/<arquivo>/<AAAA-MM-DD>_<hash>.md
   e grava historico/valve/versoes.csv (arquivo, data, commit, autor, mensagem, palavras, linhas +/-);
2. lê todas as versões do arquivo de exceções e monta dados/valve_excecoes.csv: uma linha por exceção
   individual (cada item separado por <br> ou <li>), com ano, evento, organizador inferido, categoria
   (e seção provável da regra), data e commit da primeira versão em que aparece, última versão em que
   aparece e se continua na versão atual.

Uso: python scripts/historico_valve.py [--raiz .]   (precisa do histórico completo: git fetch --unshallow)
"""
import argparse, csv, re, subprocess
from pathlib import Path

ARQUIVOS = ["tournament-operation-requirements.md", "tournament-operation-requirements-exceptions.md",
            "major-supplemental-rulebook.md", "tournament-item-submission-guidelines.md"]

ORGANIZADORES = [  # (regex no nome do evento, organizador) — inferência só quando segura
    (r"\b(ESL|IEM|ESEA|Intel Extreme|DreamHack|FACEIT)\b", "ESL FACEIT Group"),
    (r"\bBLAST\b", "BLAST"), (r"\bPGL\b", "PGL"), (r"\bCCT\b", "Grid (CCT)"),
    (r"\bElisa\b", "Elisa Esports"), (r"\bGalaxy Battle\b", "Galaxy Battle"), (r"\bYaLLa\b", "Yalla Esports"),
    (r"\bSkyesports\b", "Skyesports"), (r"\b(Hero Esports|ACL)\b", "Hero Esports"), (r"\bThunderpick\b", "Thunderpick"),
    (r"\bEWC\b|Esports World Cup", "Esports World Cup Foundation"), (r"\bStarLadder\b", "StarLadder"),
    (r"\bPerfect World\b", "Perfect World"), (r"\bFiReLEAGUE\b", "FiReLEAGUE"), (r"\bNodwin\b", "NODWIN Gaming"),
    (r"\bMajor\b", "Valve / organizador do Major"),
]

CATEGORIAS = [  # (categoria, seção provável, regex) — ordem = prioridade; confira os números na versão vigente
    ("Versão anterior dos requisitos", "preâmbulo (versão aplicável)", r"version of the Tournament Operation Requirements"),
    ("Atribuição de região a roster", "3.3.3 e regras do VRS", r"assigned to the .* region|region assignment"),
    ("Evento Wildcard", "3.9", r"Wildcard event|for the purpose of wildcard"),
    ("Qualificatórias regionais / menos convites VRS", "3.7.2", r"regional VRS qualifiers|instead of 20|in lieu of VRS invitations|teams from the VRS instead"),
    ("Filtro regional", "3.3, 3.7.1, 3.8.3", r"filter|as VRS filters|not being official regions"),
    ("Convites diretos ou extras", "3.2, 3.6", r"invite|invitation"),
    ("Premiação", "3.2.8, 4.3.2", r"prize pool|third/fourth place|performance based"),
    ("Mudanças após o prazo de Additional Information", "4.3.2, 5.4", r"after the additional information deadline|operate the event online|disqualification rules|adjust tournament format|update tournament format"),
    ("Prazos de anúncio e operação", "4.1, 4.3.1", r"shorter timeframe|announced after the deadline|announce event dates|invitation date|announce/operate"),
]


def git(raiz, *args):
    return subprocess.run(["git", "-C", str(raiz), *args], capture_output=True, text=True, check=True).stdout


def versoes(raiz, arquivo):
    out = git(raiz, "log", "--follow", "--reverse", "--format=%H|%ad|%an|%s", "--date=short", "--", arquivo)
    return [l.split("|", 3) for l in out.splitlines() if l.strip()]


def itens_excecoes(texto):
    ano, saida = None, []
    for linha in texto.splitlines():
        m = re.match(r"^#+\s*Exceptions for (\d{4})", linha.strip(), re.I)
        if m: ano = m.group(1); continue
        if not ano or not linha.strip().startswith("|"): continue
        cel = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(cel) < 2 or set(cel[0]) <= set(":- ") or cel[0].lower() == "event name": continue
        evento, bruto = cel[0], "|".join(cel[1:])
        partes = re.split(r"<br\s*/?>|</?li>|</?ul>", bruto)
        for p in partes:
            p = re.sub(r"<[^>]+>", "", p).strip()
            if p: saida.append((ano, evento, p))
    return saida


def classificar(txt):
    hits = [(c, s) for c, s, rx in CATEGORIAS if re.search(rx, txt, re.I)]
    return (hits[0] if hits else ("Outra / a classificar", "")), "; ".join(c for c, _ in hits)


def organizador(evento):
    for rx, org in ORGANIZADORES:
        if re.search(rx, evento, re.I): return org
    return "a verificar"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--raiz", default=".")
    raiz = Path(ap.parse_args().raiz).resolve()
    base = raiz / "historico" / "valve"; base.mkdir(parents=True, exist_ok=True)
    linhas_v, versoes_exc = [], []
    for arq in ARQUIVOS:
        pasta = base / Path(arq).stem; pasta.mkdir(exist_ok=True)
        for h, data, autor, msg in versoes(raiz, arq):
            try:
                conteudo = git(raiz, "show", f"{h}:{arq}")
            except subprocess.CalledProcessError:
                continue  # arquivo removido/renomeado nesse commit
            nome = f"{data}_{h[:8]}.md"
            (pasta / nome).write_text(f"<!-- {arq} | commit {h} | {data} | {autor} | {msg} -->\n" + conteudo, encoding="utf-8")
            stat = git(raiz, "show", "--numstat", "--format=", h, "--", arq).split()
            add, rem = (stat[0], stat[1]) if len(stat) >= 2 else ("", "")
            linhas_v.append({"arquivo": arq, "data": data, "commit": h, "autor": autor, "mensagem": msg,
                             "palavras": len(re.findall(r"\w+", conteudo)), "linhas_adicionadas": add,
                             "linhas_removidas": rem, "caminho": f"historico/valve/{Path(arq).stem}/{nome}"})
            if arq.endswith("exceptions.md"):
                versoes_exc.append((data, h, itens_excecoes(conteudo)))
    with open(base / "versoes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas_v[0])); w.writeheader(); w.writerows(linhas_v)

    primeira, ultima = {}, {}
    for data, h, itens in versoes_exc:
        for chave in itens:
            primeira.setdefault(chave, (data, h)); ultima[chave] = (data, h)
    atuais = set(versoes_exc[-1][2]) if versoes_exc else set()
    linhas_e = []
    for chave, (d1, h1) in sorted(primeira.items(), key=lambda kv: (kv[0][0], kv[1][0], kv[0][1])):
        ano, evento, txt = chave
        (cat, sec), todas = classificar(txt)
        linhas_e.append({"ano": ano, "evento": evento, "organizador_inferido": organizador(evento), "excecao": txt,
                         "categoria": cat, "secao_regra_provavel": sec, "todas_categorias": todas,
                         "data_inclusao": d1, "commit_inclusao": h1, "ultima_versao_com_item": ultima[chave][0],
                         "presente_na_versao_atual": "sim" if chave in atuais else "não"})
    (raiz / "dados").mkdir(exist_ok=True)
    with open(raiz / "dados" / "valve_excecoes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas_e[0])); w.writeheader(); w.writerows(linhas_e)
    print(f"{len(linhas_v)} versões exportadas; {len(linhas_e)} exceções individuais "
          f"({sum(l['presente_na_versao_atual'] == 'sim' for l in linhas_e)} na versão atual)")


if __name__ == "__main__":
    main()
