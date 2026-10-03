import pyodbc
import pandas as pd
from sklearn.linear_model import LinearRegression


def conectar():
    """Abre a conexão com o banco VendasDashboard."""
    drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
    odbc = [d for d in drivers if "ODBC Driver" in d]
    driver = sorted(odbc)[-1] if odbc else drivers[0]
    texto = (
        f"DRIVER={{{driver}}};SERVER=localhost;"
        "DATABASE=VendasDashboard;Trusted_Connection=yes;"
    )
    if "18" in driver:
        texto += "Encrypt=no;"
    return pyodbc.connect(texto)


def montar_variaveis(datas, ano_inicial):
    """Transforma as datas nas variáveis do modelo:
    tendência (0, 1, 2...) e uma coluna para cada mês do ano."""
    X = pd.DataFrame({"tendencia": (datas.year - ano_inicial) * 12 + datas.month - 1})
    for mes in range(2, 13):
        X[f"mes_{mes}"] = (datas.month == mes).astype(int)
    return X


# 1. Lê o faturamento mensal do SQL Server
conexao = conectar()
cursor = conexao.cursor()
cursor.execute("""
    SELECT DATEFROMPARTS(YEAR(Data), MONTH(Data), 1) AS Mes,
           SUM(Valor_Total) AS Faturamento
    FROM dbo.vendas
    WHERE Status = N'Concluída'
    GROUP BY DATEFROMPARTS(YEAR(Data), MONTH(Data), 1)
    ORDER BY Mes
""")
linhas = cursor.fetchall()
df = pd.DataFrame.from_records(linhas, columns=["Mes", "Faturamento"])
df["Mes"] = pd.to_datetime(df["Mes"])
df["Faturamento"] = df["Faturamento"].astype(float)

datas = pd.DatetimeIndex(df["Mes"])
ano_inicial = datas[0].year
X = montar_variaveis(datas, ano_inicial)
y = df["Faturamento"]

# 2. Teste do modelo: treina sem os 3 últimos meses e tenta prevê-los
modelo_teste = LinearRegression().fit(X.iloc[:-3], y.iloc[:-3])
previsto_teste = modelo_teste.predict(X.iloc[-3:])
real_teste = y.iloc[-3:].values
erro_pct = abs(previsto_teste - real_teste) / real_teste

print("TESTE DO MODELO (meses que ele não viu)")
for mes, real, prev, erro in zip(datas[-3:], real_teste, previsto_teste, erro_pct):
    print(f"  {mes:%m/%Y}  real: {real:>12,.0f}  previsto: {prev:>12,.0f}  erro: {erro:.1%}")
erro_medio = erro_pct.mean()
print(f"  Erro médio: {erro_medio:.1%}")

# 3. Modelo final: treina com todos os meses e prevê os 3 próximos
modelo = LinearRegression().fit(X, y)
futuro = pd.date_range(datas[-1] + pd.offsets.MonthBegin(1), periods=3, freq="MS")
previsao = modelo.predict(montar_variaveis(futuro, ano_inicial))

print("\nPREVISÃO")
for mes, valor in zip(futuro, previsao):
    print(f"  {mes:%m/%Y}  {valor:>12,.0f}")

# 4. Grava a previsão em uma tabela no SQL Server
cursor.execute("""
    IF OBJECT_ID('dbo.previsao_vendas') IS NULL
    CREATE TABLE dbo.previsao_vendas (
        Mes DATE PRIMARY KEY,
        Faturamento_Previsto DECIMAL(18, 2),
        Limite_Inferior DECIMAL(18, 2),
        Limite_Superior DECIMAL(18, 2),
        Erro_Medio_Teste DECIMAL(9, 4)
    )
""")
cursor.execute("DELETE FROM dbo.previsao_vendas")
for mes, valor in zip(futuro, previsao):
    cursor.execute(
        "INSERT INTO dbo.previsao_vendas VALUES (?, ?, ?, ?, ?)",
        mes.date(),
        round(float(valor), 2),
        round(float(valor * (1 - erro_medio)), 2),
        round(float(valor * (1 + erro_medio)), 2),
        round(float(erro_medio), 4),
    )
conexao.commit()
conexao.close()
print("\nPrevisão gravada na tabela dbo.previsao_vendas")