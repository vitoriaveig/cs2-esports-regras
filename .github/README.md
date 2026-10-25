# Regulamentos de Counter-Strike: corpus para pesquisa

Este repositório é um **fork de [ValveSoftware/counter-strike_rules_and_regs](https://github.com/ValveSoftware/counter-strike_rules_and_regs)**.
Os arquivos da Valve na raiz (requisitos de operação de torneios, exceções, regulamento suplementar dos Majors,
diretrizes de itens e declaração de conflito de interesses) continuam idênticos aos da Valve e são
sincronizados toda semana. Por cima deles, este fork acrescenta:

| Pasta / arquivo | O que é |
|---|---|
| `historico/valve/` | Todas as versões de cada regra da Valve, uma por commit (`<data>_<commit>.md`), e `versoes.csv` com data, autor, mensagem e linhas alteradas. |
| `dados/valve_excecoes.csv` | Base pronta das exceções concedidas pela Valve: uma linha por exceção, com ano, evento, organizador inferido, categoria, seção provável da regra, data e commit de inclusão e se ainda consta na versão atual. |
| `dados/vrs_indice.csv` | Índice das classificações publicadas no [Valve Regional Standings](https://github.com/ValveSoftware/counter-strike_regional_standings) (convite e ao vivo, por região e data), com link de leitura. |
| `catalogo/fontes.csv` | Curadoria dos demais documentos: organizadores (ESL Pro Tour, BLAST, PGL, StarLadder, EWC etc.), integridade (ESIC), eras anteriores (CS 1.6, Source, CS:GO), com **procedência** e **acesso**. |
| `textos/<id>.md` | Texto integral extraído de cada documento, com marcas `<!-- página N -->`. |
| `manifest.csv`, `secoes.csv` | Situação da coleta e índice de seções com página. |
| `comparativo/temas.csv` | Livro de códigos (33 temas, en/pt/es/id) para comparar com os corpora da [Riot](https://github.com/vitoriaveig/riot-esports-regras) e do [Free Fire](https://github.com/vitoriaveig/freefire-esports-regras). |
| `scripts/` | Coleta, histórico da Valve, índice do VRS, busca, comparação de versões e entre corpora. |

Acompanha a skill `cs2-regras-torneios` (cópia em [`skill/SKILL.md`](../skill/SKILL.md)).

## Camadas do corpus (coluna `camada`)

1. **Valve (regras do ecossistema):** requisitos que todo organizador de torneio com VRS precisa cumprir, exceções e regras dos Majors.
2. **Organizador terceiro:** regulamentos das competições em si (ESL, BLAST, PGL, StarLadder, EWC, organizadores regionais, universitários).
3. **Integridade (ESIC):** códigos de ética, conduta, anticorrupção, antidoping, procedimento disciplinar e decisões.
4. **Associação de jogadores:** CSPPA.

## Procedência

| Categoria | Significado |
|---|---|
| Oficial (repositório da Valve, sincronizado neste fork) | Arquivo da Valve, idêntico ao original. |
| Oficial (site do organizador / da ESIC) | Publicado por quem organiza ou regula. |
| Cópia comunitária (Liquipedia Commons) | Enviado por usuários da Liquipedia, em geral sem fonte declarada. Usar com essa ressalva. |
| Cópia em repositório de terceiros | Scribd etc. Catalogado, não coletado. |
| Cópia fornecida pela pesquisadora | PDF sem link público; o texto é versionado, o PDF não. |

Atenção: o rulebook da ESL Pro Tour fica num único arquivo do Google Drive que a ESL atualiza desde 2023 (mesmo link). As versões anteriores não estão disponíveis publicamente; o histórico passa a existir a partir das coletas semanais deste repositório (veja o `sha256` no `manifest.csv` e o histórico do Git).

## Atualização automática

O workflow semanal (segunda-feira) sincroniza com a Valve, refaz o histórico e a base de exceções, atualiza
o índice do VRS e coleta os documentos novos do catálogo. Também roda quando `catalogo/fontes.csv` ou os
scripts mudam, e pode ser disparado na aba **Actions**.

## Uso

```bash
pip install -r requirements.txt     # e poppler-utils no sistema
python scripts/historico_valve.py && python scripts/indice_vrs.py
python scripts/gerar_catalogo.py && python scripts/baixar_e_extrair.py

python scripts/buscar.py --remoto vitoriaveig/cs2-esports-regras "coach" --competicao Major
python scripts/comparar_versoes.py esl-one-cs-go-rulebook-2019 esl-one-cs-go-rulebook-2020
python scripts/comparar_corpora.py --cs-era CS2      # CS × Riot × Free Fire
```

Para incluir um documento: com link público, acrescente uma linha em `catalogo/fontes.csv`; sem link público,
use `scripts/incluir_arquivo_local.py` (veja o cabeçalho do script).

## Limitações

- Fora a camada da Valve, o corpus é curado e incompleto; ausência de documento não é ausência de regra.
- Muitos regulamentos de organizadores só existem como cópias comunitárias; confira versão e data no texto.
- A categoria e o organizador das exceções da Valve são inferidos automaticamente; confira antes de usar como variável.
- As regras da Valve regulam organizadores (requisitos para torneios), enquanto os regulamentos de organizadores regulam equipes e jogadores; compare camadas com cuidado.

## Licença e créditos

Os arquivos da Valve pertencem à Valve. Os demais textos pertencem aos respectivos autores. Os scripts deste
fork (pastas `scripts/`) estão sob licença MIT.

> Corpus organizado em: SOBRENOME, Nome. *cs2-esports-regras*. GitHub, 2026. Disponível em: https://github.com/vitoriaveig/cs2-esports-regras (commit `<hash>`).
