# EDA DataSUS: Morbidade Hospitalar no Amazonas

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Status](https://img.shields.io/badge/status-concluido-green)
![Fonte](https://img.shields.io/badge/fonte-DATASUS%20%2B%20IBGE-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Análise exploratória de dados de internações hospitalares do SUS para residentes no Amazonas, usando dados agregados do SIH/SUS via TABNET e população municipal do IBGE.

O projeto mostra um fluxo completo de análise de dados: coleta em fonte pública, padronização, limpeza, integração com base externa, construção de indicadores, visualização, documentação e um dashboard simples em Streamlit.

![Ranking por volume x taxa populacional](data/processed/ranking_volume_vs_taxa.png)

## Resumo executivo

Entre 2021 e 2025, foram analisadas **1.137.197 internações hospitalares** e **41.441 óbitos hospitalares** de residentes no Amazonas registrados no SIH/SUS.

O volume anual subiu de **215.288 internações em 2021** para **261.018 em 2025**, crescimento de aproximadamente **21,2%**. Manaus concentrou **52,8%** das internações do período, mas o ranking muda quando o volume é ajustado pela população: municípios menores, como Anamã, Silves e Ipixuna, aparecem com taxas anuais médias mais altas por 100 mil habitantes.

Por faixa etária, o maior volume absoluto está entre **20 a 29 anos** e **30 a 39 anos**. Já a mortalidade hospitalar ponderada pelo volume de internações é mais alta nas faixas de **80 anos e mais**, **70 a 79 anos** e **60 a 69 anos**.

## Perguntas orientadoras

- Como as internações hospitalares evoluíram entre 2021 e 2025?
- Quais municípios concentram a maior parte da demanda hospitalar registrada no SIH/SUS?
- Quais faixas etárias concentram maior volume de internações?
- A mortalidade hospitalar acompanha o volume de internações ou revela outro padrão?
- O ranking municipal muda quando as internações são ajustadas pela população?
- Quais limitações devem ser consideradas antes de transformar a análise em decisão?

## Fontes dos dados

Os dados foram obtidos em fontes públicas:

- **DATASUS/TABNET**: Morbidade Hospitalar do SUS (SIH/SUS), por local de residência.
- **Formulário TABNET usado pelo script**: `http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/nram.def`
- **População municipal**: API de agregados do IBGE, usando estimativas populacionais e Censo Demográfico 2022.
- **Abrangência geográfica**: Amazonas.
- **Análise principal**: anos completos de atendimento de 2021 a 2025.

Os arquivos do TABNET foram consultados por período de processamento de Jan/2021 a Fev/2026. Como o retorno também pode conter anos de atendimento fora do recorte principal, o notebook filtra a análise final para 2021-2025.

## Metodologia

1. Baixa de tabelas agregadas do TABNET em formato `prn`, separadas por `;`.
2. Salvamento dos retornos como CSV UTF-8 com metadados de fonte.
3. Limpeza e normalização no notebook:
   - remoção da linha `Total` para evitar dupla contagem;
   - conversão de entidades HTML, como `Munic&iacute;pio`;
   - transformação de tabelas largas por ano em formato longo;
   - conversão de `-` para zero;
   - conversão de números e taxas com vírgula decimal;
   - separação do código IBGE e nome do município.
4. Integração com população municipal do IBGE.
5. Cálculo de indicadores anuais, municipais, etários e de mortalidade.
6. Cálculo de taxa anual média por 100 mil habitantes em rankings agregados, usando população-ano como denominador.
7. Geração de visualizações e exportação dos CSVs tratados para `data/processed/`.

## Principais resultados

- **1.137.197 internações** foram analisadas no período 2021-2025.
- **41.441 óbitos hospitalares** foram registrados no mesmo recorte.
- O total anual cresceu **21,2%**, de 215.288 internações em 2021 para 261.018 em 2025.
- **Manaus** concentrou **52,8%** das internações; os cinco primeiros municípios concentraram **64,5%**.
- Os maiores volumes municipais foram Manaus, Parintins, Manacapuru, Itacoatiara e Tefé.
- O ranking por taxa anual média por 100 mil habitantes destacou municípios menores, como Anamã, Silves, Ipixuna, Parintins e Tefé.
- As faixas de **20 a 29 anos** e **30 a 39 anos** concentraram o maior volume de internações.
- A mortalidade hospitalar ponderada foi maior em **80 anos e mais**, **70 a 79 anos** e **60 a 69 anos**.
- A matriz volume x mortalidade mostra que municípios com muitos óbitos absolutos não são necessariamente os mesmos com maior mortalidade proporcional.

## Visualizações

### Internações por município

![Internações por município](data/processed/internacoes_municipio.png)

### Concentração territorial

![Pareto de municípios](data/processed/pareto_municipios.png)

### Volume absoluto x taxa populacional

![Ranking por volume x taxa populacional](data/processed/ranking_volume_vs_taxa.png)

### Volume x mortalidade

![Matriz volume x mortalidade](data/processed/matriz_volume_mortalidade.png)

## Estrutura do projeto

```text
.
├── data/
│   ├── raw/          # CSVs baixados do TABNET e IBGE
│   └── processed/    # CSVs limpos, rankings e gráficos gerados
├── docs/
│   ├── avaliacao_tecnica.md
│   └── dicionario_dados.md
├── notebooks/
│   └── eda_datasus_amazonas.ipynb
├── scripts/
│   ├── download_tabnet.py
│   ├── download_population_ibge.py
│   └── create_notebook.py
├── app.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Como executar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Para baixar novamente os dados:

```bash
python scripts/download_tabnet.py
python scripts/download_population_ibge.py
```

Depois execute o notebook:

```bash
jupyter notebook notebooks/eda_datasus_amazonas.ipynb
```

Para abrir o dashboard:

```bash
streamlit run app.py
```

## Dados gerados

O notebook exporta bases tratadas, resumos e gráficos para `data/processed/`. Os principais arquivos são:

- `municipios_tratados.csv`: base municipal por ano com internações, óbitos, população e taxas.
- `resumo_ano.csv`: totais anuais de internações, óbitos e indicadores por 100 mil habitantes.
- `ranking_municipios.csv`: ranking agregado por município no período 2021-2025.
- `ranking_volume_vs_taxa.csv`: comparação entre volume absoluto e taxa anual média por 100 mil habitantes.
- `resumo_faixa_etaria.csv`: internações acumuladas por faixa etária.
- `resumo_taxa_mortalidade_faixa.csv`: mortalidade hospitalar ponderada por faixa etária.
- `crescimento_municipios.csv`: variação municipal entre 2021 e 2025.
- `matriz_volume_mortalidade.csv`: classificação dos municípios por volume e mortalidade.

O dicionário das colunas está em [docs/dicionario_dados.md](docs/dicionario_dados.md).

## Dashboard Streamlit

O dashboard em `app.py` permite filtrar anos, municípios e faixas etárias, além de visualizar:

- indicadores agregados;
- série anual de internações;
- ranking municipal filtrado;
- internações por faixa etária;
- comparação entre volume absoluto e taxa anual média por 100 mil habitantes.

## Limitações

Os dados representam internações registradas no SIH/SUS e não cobrem toda a rede privada fora do SUS. A base usada é agregada, então não permite inferência causal nem análise individual.

As taxas por 100 mil habitantes reduzem o viés de comparar apenas volumes absolutos, mas não controlam estrutura etária, oferta hospitalar, perfil diagnóstico, complexidade assistencial ou fluxo regional de pacientes. Para 2023, a população municipal foi interpolada entre o Censo 2022 e a estimativa 2024.

## Próximos passos

- Adicionar recortes por sexo, capítulo CID-10, lista de morbidade e caráter de atendimento.
- Comparar Amazonas com outros estados da região Norte.
- Incluir mapas municipais e indicadores geográficos no dashboard.
- Adicionar testes simples para validar formato, chaves e totais dos CSVs gerados.
- Evoluir o Streamlit com busca por município e comparação entre dois territórios.

## Avaliação técnica

Uma leitura técnica do projeto, com pontos fortes, limitações e próximos passos, está disponível em [docs/avaliacao_tecnica.md](docs/avaliacao_tecnica.md).
