# Dicionário de dados

Este documento descreve as principais colunas dos arquivos tratados em `data/processed/`.

## Arquivos principais

- `municipios_tratados.csv`: base municipal em formato longo, com internações, óbitos, população e indicadores por ano.
- `ranking_municipios.csv`: ranking agregado por município no período analisado.
- `ranking_volume_vs_taxa.csv`: comparação entre ranking por volume absoluto e ranking por internações por 100 mil habitantes.
- `resumo_faixa_etaria.csv`: internações acumuladas por faixa etária.
- `resumo_ano.csv`: indicadores anuais agregados para o Amazonas.
- `matriz_volume_mortalidade.csv`: classificação dos municípios por volume de internações e mortalidade hospitalar.

## Colunas

| Coluna | Tipo esperado | Descrição |
|---|---:|---|
| `codigo_municipio` | texto | Código IBGE de 6 dígitos usado pelo TABNET para identificar o município. |
| `municipio` | texto | Nome do município. |
| `ano` | inteiro | Ano de atendimento analisado. A análise principal usa 2021 a 2025. |
| `populacao` | inteiro | População municipal usada como denominador para taxas por habitante. |
| `fonte_populacao` | texto | Fonte do dado populacional. Para 2023, a população é interpolada entre Censo 2022 e estimativa 2024. |
| `internacoes` | numérico | Quantidade de internações hospitalares registradas no SIH/SUS. |
| `obitos` | numérico | Quantidade de óbitos hospitalares registrados no SIH/SUS. |
| `taxa_mortalidade` | numérico | Óbitos divididos por internações, multiplicado por 100. |
| `internacoes_por_100k` | numérico | Internações divididas pela população, multiplicado por 100.000. |
| `obitos_por_100k` | numérico | Óbitos divididos pela população, multiplicado por 100.000. |
| `participacao_%` | numérico | Participação percentual do município no total de internações do período. |
| `participacao_acumulada_%` | numérico | Soma acumulada da participação percentual no ranking municipal. |
| `populacao_media` | numérico | Média da população municipal no período analisado, usada em rankings agregados. |
| `rank_volume` | inteiro | Posição do município no ranking por volume absoluto de internações. |
| `rank_taxa_100k` | inteiro | Posição do município no ranking por internações por 100 mil habitantes. |
| `diferenca_rank` | inteiro | Diferença entre ranking por volume e ranking por taxa populacional. |
| `faixa_etaria` | texto | Faixa etária agregada conforme classificação do TABNET. |

## Observações metodológicas

- A linha `Total` exportada pelo TABNET foi removida para evitar dupla contagem.
- Valores `-` do TABNET foram tratados como zero.
- Entidades HTML nos nomes das colunas foram convertidas para texto legível.
- O recorte de 2026 foi baixado, mas não usado na análise anual principal por estar incompleto.
- As taxas por 100 mil habitantes reduzem o viés de comparar apenas volumes absolutos, mas ainda não controlam estrutura etária, oferta hospitalar ou fluxo regional de pacientes.
