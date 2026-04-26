# Avaliação técnica do projeto

Este documento resume a leitura do projeto como uma entrega técnica de portfólio para uma vaga de estágio ou posição inicial em dados.

## Pontos fortes

- Usa uma fonte pública real, o DATASUS/TABNET, em vez de uma base pronta de tutorial.
- Mantém dados brutos em `data/raw/` e dados tratados em `data/processed/`, deixando clara a etapa de transformação.
- Automatiza o download dos dados com `scripts/download_tabnet.py`.
- Registra o fluxo analítico em notebook executável e versionado.
- Inclui limpeza de tipos, tratamento de valores ausentes, remoção de totais agregados e conversão de entidades HTML.
- Vai além de gráficos descritivos básicos ao incluir:
  - concentração territorial;
  - análise de Pareto;
  - crescimento municipal entre 2021 e 2025;
  - composição por faixa etária;
  - matriz volume x mortalidade.
- Exporta gráficos e tabelas finais, facilitando leitura do projeto no GitHub sem exigir execução local.

## Limitações assumidas

- A análise usa volumes absolutos, sem ajuste por população municipal.
- Os dados representam internações registradas no SIH/SUS, não toda a rede privada fora do SUS.
- O recorte de 2026 foi baixado, mas não usado na análise anual principal por estar incompleto.
- A base agregada não permite inferir causalidade.
- Sem cruzamentos por sexo, diagnóstico, procedimento ou estabelecimento, algumas hipóteses permanecem apenas interpretativas.

## Próximos passos recomendados

- Integrar população municipal do IBGE para calcular taxas por 100 mil habitantes.
- Adicionar recortes por sexo, capítulo CID-10 e lista de morbidade.
- Comparar Amazonas com outros estados da região Norte.
- Criar um painel simples em Streamlit ou Power BI com os principais indicadores.
- Adicionar testes simples para validar o formato esperado dos CSVs gerados.

## Como o projeto conversa com uma vaga de dados

O projeto evidencia competências importantes para análise e engenharia de dados em nível inicial:

- coleta de dados em fonte pública;
- padronização e limpeza;
- transformação de dados para formato analítico;
- geração de indicadores;
- visualização;
- documentação;
- comunicação de limitações.

O ponto mais forte para portfólio é mostrar o caminho completo entre dado bruto e insight final, com arquivos intermediários e resultados reproduzíveis.
