# VitrineBR | Dashboard de Vendas

Projeto de portfólio que simula as vendas de um varejo com canais online e loja física. O objetivo é mostrar o fluxo completo de análise: do banco de dados até o painel de indicadores, incluindo uma previsão de vendas.

![Dashboard VitrineBR - Visão Geral](dashboard_visao_geral.png)

## Tecnologias

- **SQL Server**: banco de dados e consultas de análise
- **Power BI**: construção do dashboard
- **DAX**: medidas, inteligência de tempo e insights automáticos
- **HTML e CSS**: painéis personalizados, gerados por medidas DAX e exibidos no visual HTML Content
- **Python** (pandas, pyodbc, scikit-learn): leitura do banco e previsão de vendas

## O que o dashboard responde

- Qual o tamanho do negócio? Faturamento, ticket médio e volume de vendas
- Estamos crescendo? Evolução dos últimos 12 meses, com média e mês de pico
- O que esperar? Previsão do próximo trimestre
- Onde vendemos mais? Ranking por região e por categoria
- O que merece atenção? Insights gerados automaticamente a partir dos dados

## Previsão de vendas

O script `02_previsao.py` lê o faturamento mensal direto do SQL Server, treina uma regressão linear com tendência e sazonalidade mensal, e grava a previsão dos três meses seguintes na tabela `previsao_vendas`, que o Power BI consome.

Para medir a qualidade do modelo, os três últimos meses da base foram escondidos no treino e depois comparados com a previsão:

| Mês | Real | Previsto | Erro |
|---|---|---|---|
| out/2025 | R$ 829.992 | R$ 666.841 | 19,7% |
| nov/2025 | R$ 1.389.673 | R$ 1.376.883 | 0,9% |
| dez/2025 | R$ 1.466.082 | R$ 1.476.411 | 0,7% |

Erro médio de 7,1%. O modelo acerta bem os meses de pico, que seguem um padrão sazonal claro, e erra mais em outubro de 2025, que ficou acima do padrão do ano anterior.

## Destaques técnicos

- Todos os painéis são medidas DAX que montam HTML dinamicamente
- Gráfico de colunas construído em HTML, com linha de média e barras de previsão
- Painel de insights com frases que se atualizam conforme os dados
- Comparação com o mês anterior baseada no último mês fechado
- Integração Python, SQL Server e Power BI: o modelo grava no banco e o dashboard lê

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `medidas_dax.md` | Todas as medidas DAX do projeto |
| `01_ler_dados.py` | Leitura do faturamento mensal no SQL Server |
| `02_previsao.py` | Modelo de previsão, teste e gravação no banco |
| `dashboard_visao_geral.png` | Print da página Visão Geral |

## Próximas etapas

- Página de análise de devoluções
- Página de produtos e canais

## Observação

Os dados são fictícios, criados apenas para fins de estudo.

## Autor

**Darlan Alves da Silva**
Analista de Logística | Power BI, SQL, DAX e Python
[LinkedIn](https://www.linkedin.com/in/darlan-alves-logistica-dados)
