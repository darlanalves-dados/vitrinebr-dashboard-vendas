import pyodbc
import pandas as pd

# 1. Escolhe o driver do SQL Server instalado no computador
drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
odbc = [d for d in drivers if "ODBC Driver" in d]
driver = sorted(odbc)[-1] if odbc else drivers[0]
print("Driver usado:", driver)

# 2. Monta a conexão com o banco
conexao_texto = (
    f"DRIVER={{{driver}}};"
    "SERVER=localhost;"
    "DATABASE=VendasDashboard;"
    "Trusted_Connection=yes;"
)
if "18" in driver:
    conexao_texto += "Encrypt=no;"

conexao = pyodbc.connect(conexao_texto)

# 3. Consulta: faturamento por mês, só vendas concluídas
consulta = """
SELECT
    DATEFROMPARTS(YEAR(Data), MONTH(Data), 1) AS Mes,
    SUM(Valor_Total) AS Faturamento,
    COUNT(*) AS Qtd_Vendas
FROM dbo.vendas
WHERE Status = N'Concluída'
GROUP BY DATEFROMPARTS(YEAR(Data), MONTH(Data), 1)
ORDER BY Mes
"""

# 4. Traz o resultado para uma tabela do pandas
df = pd.read_sql(consulta, conexao)
conexao.close()

# 5. Mostra o resultado
print(df)
print("Meses na base:", len(df))
print("Faturamento total:", round(df["Faturamento"].sum(), 2))