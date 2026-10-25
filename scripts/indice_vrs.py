#!/usr/bin/env python3
"""Índice das classificações publicadas no repositório Valve Regional Standings (VRS).

O repositório ValveSoftware/counter-strike_regional_standings tem milhares de arquivos (classificações
de convite e "ao vivo" por região e data). Em vez de copiá-los, este script lista os caminhos sem baixar
o conteúdo (clone parcial) e grava dados/vrs_indice.csv com: tipo (invitation/live), ano, região, data,
caminho e URL de leitura. Use o índice para baixar só as classificações necessárias à análise
(ex.: as de convite usadas por um Major).

Uso: python scripts/indice_vrs.py [--raiz .]
"""
import argparse, csv, re, subprocess, tempfile
from pathlib import Path

REPO = "https://github.com/ValveSoftware/counter-strike_regional_standings.git"
RAW = "https://raw.githubusercontent.com/ValveSoftware/counter-strike_regional_standings/main/"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--raiz", default=".")
    raiz = Path(ap.parse_args().raiz)
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout", REPO, d], check=True)
        commit = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        arquivos = subprocess.run(["git", "-C", d, "ls-tree", "-r", "--name-only", "HEAD"], capture_output=True, text=True).stdout.splitlines()
    linhas = []
    for p in arquivos:
        m = re.search(r"(invitation|live)/(\d{4})/standings_([a-z]+)_(\d{4})_(\d{2})_(\d{2})\.md$", p)
        if m:
            linhas.append({"tipo": m.group(1), "ano": m.group(2), "regiao": m.group(3),
                           "data": f"{m.group(4)}-{m.group(5)}-{m.group(6)}", "caminho": p, "url": RAW + p})
    linhas.sort(key=lambda l: (l["tipo"], l["data"], l["regiao"]))
    (raiz / "dados").mkdir(exist_ok=True)
    with open(raiz / "dados" / "vrs_indice.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["tipo", "ano", "regiao", "data", "caminho", "url"]); w.writeheader(); w.writerows(linhas)
    (raiz / "dados" / "vrs_indice_commit.txt").write_text(commit + "\n", encoding="utf-8")
    print(f"{len(linhas)} classificações indexadas (commit {commit[:10]})")


if __name__ == "__main__":
    main()
