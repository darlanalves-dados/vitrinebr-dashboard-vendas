# VitrineBR | Dashboard de Vendas

Projeto de portfólio que simula as vendas de um varejo com canais online e loja física. O objetivo é mostrar o fluxo completo de análise de dados: do banco de dados até o painel de indicadores.

## Tecnologias

- **SQL Server**: modelagem do banco e criação das views de análise
- **Power BI**: construção do dashboard
- **DAX**: medidas e indicadores
- **Python**: geração e tratamento dos dados

## Estrutura do banco

Banco de dados: `VendasDashboard`

| View | O que entrega |
|---|---|
| `vw_vendas_mes` | Faturamento por mês |
| `vw_vendas_regiao` | Vendas por região |
| `vw_vendas_cidade` | Vendas por cidade |
| `vw_vendas_categoria` | Vendas por categoria de produto |
| `vw_devolucoes` | Devoluções |

## Perguntas que o dashboard responde

- Como o faturamento evolui mês a mês?
- Quais regiões e cidades vendem mais?
- Quais categorias têm maior participação?
- Qual o volume de devoluções?

## Dashboard

*(inserir aqui o print do dashboard)*

## Como reproduzir

1. Execute os scripts da pasta `sql` no SQL Server para criar o banco e as views.
2. Execute os scripts da pasta `python` para gerar os dados.
3. Abra o arquivo do Power BI e atualize a conexão com o seu servidor.

## Observação

Os dados são fictícios, gerados apenas para fins de estudo.

## Autor

**Darlan Alves da Silva**
Analista de Logística | Power BI, SQL e Python
[LinkedIn](https://www.linkedin.com/in/darlan-alves-logistica-dados)
