# VitrineBR | Dashboard de Vendas

Projeto de portfólio que simula as vendas de um varejo com canais online e loja física. O objetivo é mostrar o fluxo completo de análise: do banco de dados até o painel de indicadores.

![Dashboard VitrineBR - Visão Geral](dashboard_visao_geral.png)

## Tecnologias

- **SQL Server**: banco de dados e views de análise
- **Power BI**: construção do dashboard
- **DAX**: medidas, inteligência de tempo e insights automáticos
- **HTML e CSS**: painéis personalizados, gerados por medidas DAX e exibidos no visual HTML Content

## O que o dashboard responde

- Qual o tamanho do negócio? Faturamento, ticket médio e volume de vendas
- Estamos crescendo? Evolução dos últimos 12 meses, com média e mês de pico
- Onde vendemos mais? Ranking por região e por categoria
- O que merece atenção? Insights gerados automaticamente a partir dos dados

## Destaques técnicos

- Todos os painéis são medidas DAX que montam HTML dinamicamente
- Gráfico de colunas construído em HTML, com linha de média e destaque do melhor mês
- Painel de insights com frases que se atualizam conforme os dados
- Comparação com o mês anterior baseada no último mês fechado

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `medidas_dax.md` | Todas as medidas DAX do projeto |
| `banco_e_views.sql` | Estrutura do banco e views |
| `dashboard_visao_geral.png` | Print da página Visão Geral |

## Próximas etapas

- Página de análise de devoluções
- Página de produtos e canais
- Previsão de vendas com Python

## Observação

Os dados são fictícios, criados apenas para fins de estudo.

## Autor

**Darlan Alves da Silva**
Analista de Logística | Power BI, SQL e DAX
[LinkedIn](https://www.linkedin.com/in/darlan-alves-logistica-dados)
