---
name: "cs2-regras-torneios"
description: "Consulta e analisa regras de torneios de Counter-Strike: requisitos e exceções da Valve (com histórico), Majors, VRS, regulamentos de organizadores (ESL, BLAST, PGL, EWC) e códigos da ESIC; use para dúvidas pontuais ou dados e análises para pesquisa acadêmica."
---

# Regras de torneios de Counter-Strike (Valve, organizadores e integridade)

Esta skill tem três modos. Escolha pelo pedido:

- **Consulta rápida**: uma pergunta pontual ("o evento X pode fazer Y?", "quais eventos tiveram exceção de prazo?", "o que o rulebook da ESL diz sobre técnico na pausa?"). Responda na conversa, curto e direto.
- **Análise para pesquisa**: dados, contagens, padrões, evolução no tempo, tabelas, gráficos ou texto para artigo. Siga a seção 4.
- **Comparativo**: Counter-Strike × Riot × Free Fire no mesmo tema. Siga a seção 5.

Responda sempre no idioma do usuário.

## 1. Obter as fontes (sempre)

As regras mudam com frequência; nunca responda de memória. O corpus fica no fork da pesquisadora, que espelha o repositório da Valve e acrescenta o resto:

- Repositório: https://github.com/vitoriaveig/cs2-esports-regras (fork de https://github.com/ValveSoftware/counter-strike_rules_and_regs, sincronizado toda semana)
- Base para leitura: `https://raw.githubusercontent.com/vitoriaveig/cs2-esports-regras/main/`
- Regras da Valve (raiz): `tournament-operation-requirements.md`, `tournament-operation-requirements-exceptions.md`, `major-supplemental-rulebook.md`, `tournament-item-submission-guidelines.md`.
- Acréscimos: `historico/valve/versoes.csv` e uma pasta por arquivo com todas as versões; `dados/valve_excecoes.csv` (base de exceções); `dados/vrs_indice.csv` (classificações do VRS); `catalogo/fontes.csv` e `catalogo/catalogo.csv` (documentos curados, com `camada`, `era`, `regiao`, `idioma`, **procedência** e **acesso**; `catalogo/excluidos.csv` lista o que foi retirado e por quê); `manifest.csv`; `secoes.csv`; `textos/<id>.md`; `comparativo/temas.csv`; `scripts/`.

```bash
B=https://raw.githubusercontent.com/vitoriaveig/cs2-esports-regras/main
mkdir -p cs && cd cs && for s in buscar comparar_versoes comparar_corpora; do curl -sSO $B/scripts/$s.py; done
mkdir -p comparativo && curl -sS -o comparativo/temas.csv $B/comparativo/temas.csv
python3 buscar.py --remoto vitoriaveig/cs2-esports-regras --listar --competicao Major
python3 buscar.py --remoto vitoriaveig/cs2-esports-regras "coach" "pause" --qualquer --max 5
```

Filtros do buscador: `--jogo`, `--competicao`, `--temporada`, `--tipo`, `--procedencia`, `--ids`; `--regex`, `--qualquer`, `--contar`, `--max`.

Se o fork estiver indisponível, leia as regras direto da Valve (https://raw.githubusercontent.com/ValveSoftware/counter-strike_rules_and_regs/main/<arquivo>.md) ou clone o repositório da Valve. Se nada funcionar, peça ao usuário que anexe os arquivos. Confira no `manifest.csv` se cada texto está `ok`; `nao_coletado` traz o motivo em `detalhe`. Não tente contornar bloqueios de sites nem baixar de Scribd.

**Quando o usuário anexar um regulamento:** calcule o SHA-256 e compare com `manifest.csv`; se for novo, identifique evento, organizador, ano e versão nas primeiras páginas, acrescente a linha em `catalogo/fontes.csv` (`acesso` = "fornecido pela pesquisadora (texto extraído do PDF)", `procedencia` = "Cópia fornecida pela pesquisadora", `url` = `arquivo-fornecido:<nome>`), rode `python scripts/gerar_catalogo.py && python scripts/incluir_arquivo_local.py <id> <arquivo>` num clone e envie `catalogo/fontes.csv`, `textos/<id>.md` e `manifest.csv` ao GitHub. Nunca versione o PDF.

## 2. Como ler as regras

**Camadas** (coluna `camada`): (1) **Valve**: regras do ecossistema que os organizadores precisam cumprir para usar o VRS e para os Majors; (2) **organizador terceiro**: regulamento da competição, que rege equipes e jogadores (ESL Pro Tour, BLAST, PGL, StarLadder, EWC, ligas regionais e universitárias); (3) **integridade (ESIC)**: códigos que os membros da ESIC adotam; (4) **associação de jogadores** (CSPPA). A Valve regula organizadores; os organizadores regulam participantes. Em perguntas sobre conduta de jogador, o documento certo quase sempre é o do organizador; em perguntas sobre convites, prazos, premiação e formato, é a Valve.

**Versão aplicável (Valve).** Vale para um torneio a versão dos requisitos em vigor no prazo de *Additional Information* daquele torneio (preâmbulo do documento). Use `historico/valve/versoes.csv` para achar a versão vigente numa data e cite o commit. Uma regra de hoje pode não valer para um evento passado.

Torneios podem ser Ranked (Tier 1, Tier 2, Wildcard) ou Unranked. Unranked podem convidar livremente, mas têm teto de premiação.

**Exceções.** A Valve diz que a lista pode estar incompleta. Se um evento não aparece, diga "não há exceção registrada", nunca "o evento segue a regra". `dados/valve_excecoes.csv` já traz cada exceção separada, com categoria, seção provável, data e commit de inclusão e se continua na versão atual. Categoria, seção e organizador são inferidos por regras: confira e diga que é interpretação quando a ligação com a regra não for óbvia.

Mapa de tipos de exceção para a seção da regra que elas flexibilizam (confira os números das seções na versão vigente, pois podem mudar):

| Tipo de exceção | Seção provável |
|---|---|
| Convite direto por desempenho prévio, convites extras ou a times específicos | 3.2 (Invites), 3.6 (Wildcard Invite) |
| Filtros regionais (ex.: NA e SA separados) | 3.3 (VRS Subdivision), 3.7.1, 3.8.3 |
| Qualificatórias regionais no lugar de convites VRS; menos convites VRS (ex.: 16 em vez de 20) | 3.7.2 |
| Prazos de anúncio/operação menores | 4.1, 4.3.1 |
| Mudanças após o prazo de Additional Information (formato, datas, online/LAN, regras de desqualificação) | 4.3.2, 5.4 |
| Premiação: disputa de 3º lugar, divisão com prêmio por desempenho, redução da premiação anunciada | 3.2.8, 4.3.2 |
| Eventos Wildcard (ex.: após dois torneios em vez de três; qualificatória tratada como Tier 2) | 3.9 |
| Operar sob versão anterior dos requisitos | preâmbulo (versão aplicável) |
| Atribuição de região a um roster específico | 3.3.3 e regras do VRS |

Quando a relação entre a exceção e a regra não for óbvia (ex.: disputa de 3º lugar provavelmente esbarra na exigência de premiação igual para colocações iguais, 3.2.8 b), diga que é uma interpretação.

**Organizadores.** O rulebook da ESL Pro Tour é um arquivo único no Google Drive que a ESL sobrescreve desde 2023 (mesmo link); versões antigas não estão disponíveis publicamente, e o histórico só existe a partir das coletas do repositório. Desde a Update #2 de 2026 (07/07/2026) ele reúne General Rules, Game Specific Rules e Roster Restrictions. Muitos regulamentos de outras épocas são cópias comunitárias da Liquipedia: cite com a ressalva de procedência e confira versão e data no texto. Todos os documentos do catálogo foram conferidos no texto (jogo, era, região e idioma preenchidos); os que eram de outro jogo foram retirados e estão em `catalogo/excluidos.csv`, com o motivo. A planilha de posições permitidas e proibidas por mapa ("pixel walks") da ESL aparece três vezes em `dados/` (ESL Pro Tour, regras específicas do jogo e EWC 2026), com o mesmo conteúdo: conte-a uma vez só.

**VRS.** `dados/vrs_indice.csv` lista as classificações de convite e "ao vivo" por região e data, com link para cada arquivo; baixe só as necessárias (ex.: as classificações de convite usadas para um Major ou para os convites de um torneio).

**Glossário.** VRS = Valve Regional Standings; MRQ = Major Regional Qualifier; RMR = Regional Major Ranking (sistema anterior); Roster = cinco atletas específicos; Main Stage = fase a partir da qual nenhum roster entra; Additional Information = anúncio obrigatório com filtros, convites, datas, premiação e regras de desclassificação; ESIC = Esports Integrity Commission; CSPPA = associação de jogadores profissionais de CS. Eras: CS 1.6, Source, CS:GO (2012–2023) e CS2 (desde 2023).

## 3. Modo consulta rápida

1. Identifique evento, organizador e ano (há eventos com o mesmo nome em anos diferentes, ex.: BLAST Rivals 2025 e 2026).
2. Escolha a camada certa e o documento pelo catálogo; localize o trecho com `buscar.py` ou `secoes.csv`.
3. Responda em poucas linhas: a regra (com o número da seção e a página quando houver), o trecho original em inglês entre aspas com tradução, a exceção concedida se houver, a versão aplicável e a procedência.
4. Para perguntas transversais ("quais eventos..."), use `dados/valve_excecoes.csv` e liste evento, ano e exceção resumida.
5. Termine com o link do arquivo usado (GitHub ou link oficial da coluna `url`).

## 4. Modo análise para pesquisa

### 4.1 Bases prontas

- **Exceções da Valve** (`dados/valve_excecoes.csv`): contagens por categoria, ano, organizador e tier; tempo entre inclusão da exceção e o evento; exceções removidas ou alteradas (`presente_na_versao_atual` = não); exceções que viraram regra depois (compare o texto da exceção com versões posteriores dos requisitos em `historico/valve/`; exemplo a checar: a separação NA/SA, concedida como exceção em 2025 e hoje prevista como possibilidade na seção 3.3.1).
- **Se a base pronta não estiver disponível**, monte-a: clone o repositório da Valve (com histórico) e, em Python, transforme as tabelas do arquivo de exceções em uma linha por exceção individual (separe por `<br>` e por itens `<li>`, mantendo subitens ligados à exceção-mãe), com `ano`, `evento`, `organizador` (só quando seguro: ESL, IEM, ESEA → ESL FACEIT Group; BLAST → BLAST; PGL → PGL; nos demais, "a verificar"; não invente), `texto_original`, `categoria`, `secao_regra`, `tier` (se inferível), `data_inclusao` e `commit_inclusao` (via `git log --follow -p` ou `git log -S"<evento>"`). O script `scripts/historico_valve.py` do fork faz exatamente isso.
- **Histórico das regras** (`historico/valve/versoes.csv` + versões): evolução dos requisitos e do regulamento dos Majors; use `comparar_versoes.py` ou `diff` entre duas versões e cite datas e commits.
- **Organizadores**: compare regulamentos de um mesmo organizador no tempo (ex.: ESL One 2018 → 2019 → 2020; ESL Pro League 2020 em três versões; IEM XIII → XV; BLAST Premier 2020 → 2021) e organizadores entre si (Majors de ESL, PGL, StarLadder, ELEAGUE, BLAST).
- **Integridade**: códigos da ESIC e a decisão sobre o bug do técnico (2020) como dado de sanções.
- **VRS**: série histórica de classificações para relacionar convites, exceções e resultados.

### 4.2 Rigor e entrega

- Números saem de código, nunca de estimativa. Toda afirmação sobre regra cita documento, seção, página (ou commit) e procedência.
- A base codificada vai como planilha (artifact do tipo Sheets, se disponível; .xlsx só se o usuário pedir). Gráficos calculados em código.
- Nota metodológica curta, pronta para o artigo: fontes e URLs; hash do commit do fork e do repositório da Valve (`git ls-remote https://github.com/vitoriaveig/cs2-esports-regras HEAD`); data de acesso; esquema de codificação; limitações (lista de exceções mantida pela Valve e possivelmente incompleta; categorias atribuídas pelo pesquisador; cópias comunitárias; rulebook da ESL sem histórico público anterior às coletas). Sugira dupla codificação e kappa de Cohen se o artigo exigir.
- Referência no estilo que o usuário indicar (ABNT, APA etc.); se não indicar, pergunte. Inclua sempre URL, commit e data de acesso.

### 4.3 Texto acadêmico

Se o usuário pedir texto para artigo ou revisão de um texto dele: use registro acadêmico adequado a periódicos internacionais de alto impacto, melhore ortografia, coesão e fluidez e preserve a forma de escrita do autor (vocabulário, ritmo, estrutura de argumento). Não acrescente afirmações que as bases não sustentem; números citados no texto devem vir da análise feita.

## 5. Modo comparativo (Counter-Strike × Riot × Free Fire)

```bash
python3 comparar_corpora.py --cs-era CS2                 # lê os três corpora do GitHub
python3 comparar_corpora.py --cs-camada Valve --trechos apostas --max-trechos 3
```

Corpora: este (separado em Valve, organizadores de CS e ESIC), Riot (https://github.com/vitoriaveig/riot-esports-regras) e Free Fire (https://github.com/vitoriaveig/freefire-esports-regras). Livro de códigos com 30 temas e 3 marcadores deônticos em inglês, português, espanhol e indonésio. Interprete com cuidado: as camadas regulam sujeitos diferentes (organizadores × participantes), os corpora têm tamanhos e idiomas diferentes e presença de termo não é presença de regra; use os números para orientar a leitura e confirme com trechos. O dicionário não cobre os poucos textos em francês, alemão e russo (aparecem com tema ausente), e a ESIC entra com um só documento, porque as demais páginas têm menos de 300 palavras (ajuste `--min-palavras` se precisar delas). Skills relacionadas: `riot-esports-regras` e `freefire-esports-regras`.
