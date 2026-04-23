# Projeto 1 - EDA DataSUS: Morbidade Hospitalar no Amazonas

Análise exploratória de dados de morbidade hospitalar do SUS para residentes no Amazonas, com foco em município, faixa etária e ano.

## Fonte dos dados

Os dados foram obtidos no **DATASUS/TABNET**, em:

- Portal: [Morbidade Hospitalar do SUS (SIH/SUS)](https://datasus.saude.gov.br/acesso-a-informacao/morbidade-hospitalar-do-sus-sih-sus/)
- Formulário TABNET usado pelo script: `http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/nram.def`
- Abrangência: Amazonas
- Recorte: morbidade hospitalar por local de residência
- Arquivos baixados: períodos de processamento de Jan/2021 a Fev/2026
- Análise principal: anos completos de atendimento de 2021 a 2025

## Estrutura

```text
.
├── data/
│   ├── raw/          # CSVs baixados do TABNET
│   └── processed/    # CSVs limpos gerados pelo notebook
├── notebooks/
│   └── eda_datasus_amazonas.ipynb
├── scripts/
│   ├── download_tabnet.py
│   └── create_notebook.py
├── requirements.txt
└── README.md
```

## Metodologia

1. Download de tabelas agregadas do TABNET em formato `prn`, separado por `;`.
2. Padronização dos arquivos como CSV UTF-8 com metadados de fonte.
3. Limpeza no notebook:
   - remoção da linha `Total` para evitar dupla contagem;
   - conversão de entidades HTML, como `Munic&iacute;pio`;
   - transformação de anos em formato longo;
   - conversão de `-` para zero;
   - conversão de tipos numéricos e taxa com vírgula decimal;
   - separação do código IBGE e nome do município.
4. Análise por município, faixa etária e ano.
5. Visualização com Seaborn/Matplotlib.

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
```

Depois abra e execute:

```bash
jupyter notebook notebooks/eda_datasus_amazonas.ipynb
```

O notebook também gera arquivos limpos em `data/processed/`.

## Achados principais

- Entre 2021 e 2025, foram observadas **1.137.197 internações** de residentes no Amazonas.
- O total anual subiu de **215.288 internações em 2021** para **261.018 em 2025**, crescimento de aproximadamente **21,2%**.
- **Manaus concentrou 52,8%** das internações do período, seguida por Parintins, Manacapuru, Itacoatiara e Tefé.
- As faixas etárias com maior volume foram **20 a 29 anos** e **30 a 39 anos**.
- A taxa média de mortalidade hospitalar foi mais alta nas faixas **80 anos e mais**, **70 a 79 anos** e **60 a 69 anos**.

## Exemplos de visualização

![Internações por município](data/processed/internacoes_municipio.png)

## Observações

Os dados representam internações registradas no SIH/SUS e não incluem todo o atendimento privado fora do SUS. Como 2026 ainda está incompleto no momento do download, os gráficos e conclusões anuais usam 2021 a 2025.
