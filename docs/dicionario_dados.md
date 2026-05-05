# Dicionário de dados

Este documento descreve as principais colunas dos arquivos tratados em `data/processed/`.

## Arquivos principais

- `municipios_tratados.csv`: base municipal em formato longo, com internações, óbitos, população e indicadores por ano.
- `ranking_municipios.csv`: ranking agregado por município no período 2021-2025.
- `ranking_volume_vs_taxa.csv`: comparação entre ranking por volume absoluto e ranking por taxa anual média de internações por 100 mil habitantes.
- `resumo_faixa_etaria.csv`: internações acumuladas por faixa etária.
- `resumo_taxa_mortalidade_faixa.csv`: mortalidade hospitalar ponderada pelo volume de internações de cada faixa etária.
- `resumo_ano.csv`: indicadores anuais agregados para o Amazonas.
- `matriz_volume_mortalidade.csv`: classificação dos municípios por volume de internações e mortalidade hospitalar.

## Colunas

| Coluna | Tipo esperado | Descrição |
|---|---:|---|
| `codigo_municipio` | texto | Código IBGE de 6 dígitos usado pelo TABNET para identificar o município. |
| `codigo_ibge_7` | texto | Código IBGE de 7 dígitos usado pela API do IBGE. |
| `municipio` | texto | Nome do município. |
| `ano` | inteiro | Ano de atendimento analisado. A análise principal usa 2021 a 2025. |
| `populacao` | inteiro | População municipal usada como denominador para indicadores anuais. |
| `populacao_media` | numérico | Média da população municipal entre 2021 e 2025. Mantida como referência descritiva nos rankings agregados. |
| `populacao_periodo` | numérico | Soma das populações anuais do período. Aproxima população-ano e é usada como denominador nos rankings agregados por 100 mil habitantes. |
| `fonte_populacao` | texto | Fonte do dado populacional. Para 2023, a população é interpolada entre Censo 2022 e estimativa 2024. |
| `internacoes` | numérico | Quantidade de internações hospitalares registradas no SIH/SUS. |
| `obitos` | numérico | Quantidade de óbitos hospitalares registrados no SIH/SUS. |
| `obitos_estimados` | numérico | Óbitos estimados por faixa etária a partir da taxa de mortalidade do TABNET e do volume de internações. |
| `taxa_mortalidade` | numérico | Óbitos divididos por internações, multiplicado por 100. |
| `taxa_mortalidade_ponderada` | numérico | Taxa de mortalidade por faixa etária ponderada pelo volume de internações no período. |
| `internacoes_por_100k` | numérico | Internações divididas pela população e multiplicadas por 100.000. Em bases anuais, usa a população do ano. Em rankings agregados, usa `populacao_periodo`, representando taxa anual média por 100 mil habitantes. |
| `obitos_por_100k` | numérico | Óbitos divididos pela população e multiplicados por 100.000. Em rankings agregados, usa `populacao_periodo`. |
| `participacao_%` | numérico | Participação percentual do município no total de internações do período. |
| `participacao_acumulada_%` | numérico | Soma acumulada da participação percentual no ranking municipal. |
| `rank_volume` | inteiro | Posição do município no ranking por volume absoluto de internações. |
| `rank_taxa_100k` | inteiro | Posição do município no ranking por taxa anual média de internações por 100 mil habitantes. |
| `diferenca_rank` | inteiro | Diferença entre ranking por volume e ranking por taxa populacional. |
| `faixa_etaria` | texto | Faixa etária agregada conforme classificação do TABNET. |
| `grupo_volume` | texto | Classificação do município acima ou abaixo da mediana de internações, dentro da matriz volume x mortalidade. |
| `grupo_mortalidade` | texto | Classificação do município acima ou abaixo da mediana de mortalidade, dentro da matriz volume x mortalidade. |
| `quadrante` | texto | Combinação de `grupo_volume` e `grupo_mortalidade`. |

## Observações metodológicas

- A linha `Total` exportada pelo TABNET foi removida para evitar dupla contagem.
- Valores `-` do TABNET foram tratados como zero.
- Entidades HTML nos nomes das colunas foram convertidas para texto legível.
- O recorte de 2026 foi baixado, mas não usado na análise anual principal por estar incompleto.
- Nos rankings agregados de 2021-2025, `internacoes_por_100k` e `obitos_por_100k` usam população-ano como denominador. Isso evita comparar cinco anos de eventos contra apenas uma população média anual.
- As taxas por 100 mil habitantes reduzem o viés de comparar apenas volumes absolutos, mas ainda não controlam estrutura etária, oferta hospitalar ou fluxo regional de pacientes.
