# Medidas DAX | VitrineBR

Todas as medidas usadas na página **Visão Geral**. Os painéis são renderizados com o visual **HTML Content**, a partir de medidas que montam o HTML dinamicamente.

Tabelas usadas: `vendas` (uma linha por venda) e `Calendario` (tabela de datas relacionada a `vendas[Data]`).

## 1. Medidas base

```dax
Total Vendido =
CALCULATE ( SUM ( vendas[Valor_Total] ), vendas[Status] = "Concluída" )
```

```dax
Qtd Vendas =
CALCULATE ( COUNTROWS ( vendas ), vendas[Status] = "Concluída" )
```

```dax
Ticket Medio = DIVIDE ( [Total Vendido], [Qtd Vendas] )
```

```dax
% Online =
DIVIDE (
    CALCULATE ( [Total Vendido], vendas[Canal] = "Online" ),
    [Total Vendido]
)
```

## 2. Comparação mensal (último mês fechado)

```dax
Vendas Mes Atual =
VAR _ult = MAX ( vendas[Data] )
VAR _fim = IF ( _ult = EOMONTH ( _ult, 0 ), _ult, EOMONTH ( _ult, -1 ) )
VAR _ini = EOMONTH ( _fim, -1 ) + 1
RETURN
    CALCULATE (
        [Total Vendido],
        REMOVEFILTERS ( Calendario ),
        Calendario[Date] >= _ini && Calendario[Date] <= _fim
    )
```

```dax
Vendas Mes Anterior =
VAR _ult = MAX ( vendas[Data] )
VAR _fim = IF ( _ult = EOMONTH ( _ult, 0 ), _ult, EOMONTH ( _ult, -1 ) )
VAR _fimAnt = EOMONTH ( _fim, -1 )
VAR _iniAnt = EOMONTH ( _fim, -2 ) + 1
RETURN
    CALCULATE (
        [Total Vendido],
        REMOVEFILTERS ( Calendario ),
        Calendario[Date] >= _iniAnt && Calendario[Date] <= _fimAnt
    )
```

```dax
Variacao Pct = DIVIDE ( [Vendas Mes Atual] - [Vendas Mes Anterior], [Vendas Mes Anterior] )
```

```dax
Mes Referencia =
VAR _ult = MAX ( vendas[Data] )
VAR _fim = IF ( _ult = EOMONTH ( _ult, 0 ), _ult, EOMONTH ( _ult, -1 ) )
RETURN FORMAT ( _fim, "mmm/yyyy" )
```

## 3. Cabeçalho

```dax
Cabecalho HTML =
VAR _ini = CALCULATE ( MIN ( vendas[Data] ), REMOVEFILTERS ( Calendario ) )
VAR _fim = CALCULATE ( MAX ( vendas[Data] ), REMOVEFILTERS ( Calendario ) )
RETURN
"<div style='font-family:Segoe UI;background:#12239E;border-radius:18px;padding:22px 30px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 3px 14px #0f1b4d40'>"
& "<div><div style='font-size:32px;font-weight:700;color:#ffffff;letter-spacing:1px'>VitrineBR | Performance Comercial</div>"
& "<div style='font-size:17px;color:#ffffffcc;margin-top:4px'>Dashboard de vendas &#8226; Visão geral</div></div>"
& "<div style='text-align:right'><div style='font-size:15px;color:#ffffffb3;text-transform:uppercase;letter-spacing:1px'>Período analisado</div>"
& "<div style='font-size:22px;font-weight:700;color:#ffffff;margin-top:2px'>"
& FORMAT ( _ini, "mmm/yyyy", "pt-BR" ) & " a " & FORMAT ( _fim, "mmm/yyyy", "pt-BR" ) & "</div></div>"
& "</div>"
```

## 4. Faixa de cards (KPIs)

```dax
Cards KPI HTML =
VAR _tot = [Total Vendido]
VAR _qtd = [Qtd Vendas]
VAR _ticket = [Ticket Medio]
VAR _mes = [Vendas Mes Atual]
VAR _var = [Variacao Pct]
VAR _ref = [Mes Referencia]
VAR _online = [% Online]
VAR _corVar = IF ( _var >= 0, "#14804a", "#c0392b" )
VAR _seta = IF ( _var >= 0, "&#9650;", "&#9660;" )
VAR _card = "flex:1;border-radius:16px;padding:22px 24px;box-shadow:0 4px 14px #0f1b4d40;background:"
VAR _lab = "<div style='font-size:15px;letter-spacing:1px;text-transform:uppercase;color:#ffffffd9;font-weight:600'>"
VAR _val = "<div style='font-size:44px;font-weight:700;color:#ffffff;margin-top:10px;line-height:1.1'>"
VAR _sub = "<div style='font-size:15px;color:#ffffffcc;margin-top:12px'>"
RETURN
"<div style='display:flex;gap:18px;font-family:Segoe UI;padding:8px'>"
& "<div style='" & _card & "#0d1a73'>" & _lab & "Faturamento total</div>"
& _val & "R$ " & FORMAT ( _tot / 1000000, "0.0", "pt-BR" ) & " Mi</div>"
& _sub & "Vendas concluídas no período</div></div>"

& "<div style='" & _card & "#12239E'>" & _lab & "Vendas em " & _ref & "</div>"
& _val & "R$ " & FORMAT ( _mes / 1000000, "0.00", "pt-BR" ) & " Mi</div>"
& "<span style='display:inline-block;margin-top:12px;padding:4px 12px;border-radius:20px;font-size:15px;font-weight:700;background:#ffffff;color:" & _corVar & "'>"
& _seta & " " & FORMAT ( ABS ( _var ), "0.0%", "pt-BR" ) & "</span>"
& "<span style='font-size:15px;color:#ffffffcc;margin-left:8px'>vs. mês anterior</span></div>"

& "<div style='" & _card & "#1a36b8'>" & _lab & "Ticket médio</div>"
& _val & "R$ " & FORMAT ( _ticket, "#,0", "pt-BR" ) & "</div>"
& _sub & "Valor médio por venda</div></div>"

& "<div style='" & _card & "#2450d0'>" & _lab & "Vendas realizadas</div>"
& _val & FORMAT ( _qtd, "#,0", "pt-BR" ) & "</div>"
& _sub & "Pedidos concluídos</div></div>"

& "<div style='" & _card & "#2f66de'>" & _lab & "Canal online</div>"
& _val & FORMAT ( _online, "0%", "pt-BR" ) & "</div>"
& "<div style='height:11px;background:#ffffff4d;border-radius:6px;margin-top:14px;overflow:hidden'>"
& "<div style='height:11px;width:" & FORMAT ( _online * 100, "0" ) & "%;background:#ffffff'></div></div>"
& _sub & "Loja física: " & FORMAT ( 1 - _online, "0%", "pt-BR" ) & "</div></div>"
& "</div>"
```

## 5. Evolução do faturamento (12 meses, com linha de média)

```dax
Grafico Mensal HTML =
VAR _fim = EOMONTH ( MAX ( vendas[Data] ), 0 )
VAR _t1 =
    ADDCOLUMNS ( GENERATESERIES ( 0, 11, 1 ), "@fim", EOMONTH ( _fim, [Value] - 11 ) )
VAR _t2 =
    ADDCOLUMNS (
        _t1,
        "@val",
            VAR _f = [@fim]
            VAR _i = EOMONTH ( _f, -1 ) + 1
            RETURN
                CALCULATE (
                    [Total Vendido],
                    REMOVEFILTERS ( Calendario ),
                    Calendario[Date] >= _i && Calendario[Date] <= _f
                )
    )
VAR _max = MAXX ( _t2, [@val] )
VAR _med = AVERAGEX ( _t2, [@val] )
VAR _melhor = MAXX ( FILTER ( _t2, [@val] = _max ), [@fim] )
VAR _alt = 280
VAR _yMed = ROUND ( DIVIDE ( _med, _max ) * _alt, 0 ) + 34
VAR _barras =
    CONCATENATEX (
        _t2,
        VAR _h = ROUND ( DIVIDE ( [@val], _max ) * _alt, 0 ) + 0
        VAR _cor =
            IF ( [@val] = _max, "#12239E", IF ( [@val] >= _med, "#4d7cf0", "#b9c8f7" ) )
        RETURN
            "<div style='flex:1;text-align:center'>"
                & "<div style='margin-bottom:6px;position:relative;z-index:2'>"
                & "<span style='font-size:17px;font-weight:700;color:#1f2a60;background:#ffffff;padding:0 6px;border-radius:6px'>"
                & FORMAT ( [@val] / 1000000, "0.0", "pt-BR" ) & "</span></div>"
                & "<div style='height:" & _h & "px;background:" & _cor & ";border-radius:8px 8px 0 0;margin:0 10px'></div>"
                & "<div style='height:26px;line-height:26px;margin-top:8px;font-size:16px;font-weight:600;color:#7a84a6;text-transform:uppercase'>"
                & FORMAT ( [@fim], "mmm", "pt-BR" ) & "</div>"
                & "</div>",
        "",
        [Value], ASC
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24;box-sizing:border-box'>"
& "<div style='display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center'>"
& "<div><div style='font-size:24px;font-weight:700;color:#1f2a60'>Evolução do faturamento</div>"
& "<div style='font-size:16px;color:#8a93b2;margin-top:2px'>Últimos 12 meses, em R$ milhões</div></div>"
& "<div style='display:flex;gap:10px'>"
& "<div style='font-size:15px;font-weight:600;color:#c0392b;background:#fdeaea;padding:7px 14px;border-radius:20px'>Média: R$ "
& FORMAT ( _med / 1000000, "0.00", "pt-BR" ) & " Mi</div>"
& "<div style='font-size:15px;font-weight:600;color:#12239E;background:#e8ecfb;padding:7px 14px;border-radius:20px'>Pico: "
& FORMAT ( _melhor, "mmm/yyyy", "pt-BR" ) & "</div>"
& "</div></div>"
& "<div style='position:relative;display:flex;align-items:flex-end;height:350px;margin-top:14px'>"
& "<div style='position:absolute;left:0;right:0;bottom:" & _yMed & "px;border-top:2px dashed #E85D5D;z-index:1'></div>"
& _barras
& "</div></div>"
```

## 6. Insights automáticos

```dax
Insights HTML =
VAR _tot = [Total Vendido]
VAR _tReg = ADDCOLUMNS ( VALUES ( vendas[Regiao] ), "@v", [Total Vendido] )
VAR _vReg = MAXX ( _tReg, [@v] )
VAR _topReg = MAXX ( FILTER ( _tReg, [@v] = _vReg ), vendas[Regiao] )
VAR _tCat = ADDCOLUMNS ( VALUES ( vendas[Categoria] ), "@v", [Total Vendido] )
VAR _vCat = MAXX ( _tCat, [@v] )
VAR _topCat = MAXX ( FILTER ( _tCat, [@v] = _vCat ), vendas[Categoria] )
VAR _fim = EOMONTH ( MAX ( vendas[Data] ), 0 )
VAR _t1 = ADDCOLUMNS ( GENERATESERIES ( 0, 11, 1 ), "@fim", EOMONTH ( _fim, [Value] - 11 ) )
VAR _t2 =
    ADDCOLUMNS (
        _t1,
        "@val",
            VAR _f = [@fim]
            VAR _i = EOMONTH ( _f, -1 ) + 1
            RETURN
                CALCULATE (
                    [Total Vendido],
                    REMOVEFILTERS ( Calendario ),
                    Calendario[Date] >= _i && Calendario[Date] <= _f
                )
    )
VAR _max = MAXX ( _t2, [@val] )
VAR _med = AVERAGEX ( _t2, [@val] )
VAR _melhor = MAXX ( FILTER ( _t2, [@val] = _max ), [@fim] )
VAR _online = [% Online]
VAR _dev = CALCULATE ( COUNTROWS ( vendas ), vendas[Status] = "Devolvida" )
VAR _taxa = DIVIDE ( _dev, COUNTROWS ( vendas ) )
VAR _box = "<div style='flex:1 1 30%;border-radius:14px;padding:18px 20px;background:"
VAR _lab = "'><div style='font-size:15px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#5c6690'>"
VAR _num = "</div><div style='font-size:46px;font-weight:700;line-height:1.1;margin-top:6px;color:"
VAR _txt = "</div><div style='font-size:18px;color:#3d4770;margin-top:8px;line-height:1.35'>"
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='font-size:24px;font-weight:700;color:#1f2a60'>Principais insights</div>"
& "<div style='font-size:16px;color:#8a93b2;margin-top:2px'>Gerados automaticamente a partir dos dados</div>"
& "<div style='display:flex;flex-wrap:wrap;gap:16px;margin-top:18px'>"

& _box & "#f1f4fc" & _lab & "Concentração regional" & _num & "#12239E'>"
& FORMAT ( DIVIDE ( _vReg, _tot ), "0%", "pt-BR" ) & _txt
& "do faturamento vem do <b>" & _topReg & "</b>, com R$ " & FORMAT ( _vReg / 1000000, "0.0", "pt-BR" ) & " Mi.</div></div>"

& _box & "#f1f4fc" & _lab & "Categoria líder" & _num & "#12239E'>"
& FORMAT ( DIVIDE ( _vCat, _tot ), "0%", "pt-BR" ) & _txt
& "das vendas são de <b>" & _topCat & "</b>, com R$ " & FORMAT ( _vCat / 1000000, "0.0", "pt-BR" ) & " Mi.</div></div>"

& _box & "#e6f6ed" & _lab & "Sazonalidade" & _num & "#0f7a47'>+"
& FORMAT ( DIVIDE ( _max, _med ) - 1, "0%", "pt-BR" ) & _txt
& "acima da média em <b>" & FORMAT ( _melhor, "mmm/yyyy", "pt-BR" ) & "</b>, o melhor mês do período.</div></div>"

& _box & "#f1f4fc" & _lab & "Canal de venda" & _num & "#12239E'>"
& FORMAT ( _online, "0%", "pt-BR" ) & _txt
& "do faturamento vem do <b>canal online</b>, contra " & FORMAT ( 1 - _online, "0%", "pt-BR" ) & " da loja física.</div></div>"

& _box & "#fdf3e0" & _lab & "Devoluções" & _num & "#b36b00'>"
& FORMAT ( _taxa, "0.0%", "pt-BR" ) & _txt
& "dos pedidos foram devolvidos: <b>" & FORMAT ( _dev, "#,0", "pt-BR" ) & " vendas</b>. Ponto de atenção.</div></div>"

& "</div></div>"
```

## 7. Ranking por região

```dax
Ranking Regiao HTML =
VAR _tot = [Total Vendido]
VAR _t = ADDCOLUMNS ( VALUES ( vendas[Regiao] ), "@v", [Total Vendido] )
VAR _max = MAXX ( _t, [@v] )
VAR _linhas =
    CONCATENATEX (
        _t,
        VAR _atual = [@v]
        VAR _pos = COUNTROWS ( FILTER ( _t, [@v] > _atual ) ) + 1
        VAR _w = ROUND ( DIVIDE ( [@v], _max ) * 100, 0 ) + 0
        VAR _cor = IF ( [@v] = _max, "#12239E", "#4d7cf0" )
        RETURN
            "<div style='margin-top:20px'>"
                & "<div style='display:flex;justify-content:space-between;font-size:18px'>"
                & "<span style='font-weight:700;color:#1f2a60'>" & _pos & "º &nbsp;" & vendas[Regiao] & "</span>"
                & "<span style='color:#5c6690;font-weight:600'>R$ " & FORMAT ( [@v] / 1000000, "0.0", "pt-BR" ) & " Mi &nbsp;|&nbsp; "
                & FORMAT ( DIVIDE ( [@v], _tot ), "0%", "pt-BR" ) & "</span></div>"
                & "<div style='height:14px;background:#e8ebf5;border-radius:8px;margin-top:8px;overflow:hidden'>"
                & "<div style='height:14px;width:" & _w & "%;background:" & _cor & ";border-radius:8px'></div></div>"
                & "</div>",
        "",
        [@v], DESC
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='font-size:24px;font-weight:700;color:#1f2a60'>Faturamento por região</div>"
& "<div style='font-size:16px;color:#8a93b2;margin-top:2px'>Valor e participação no total</div>"
& _linhas
& "</div>"
```

## 8. Ranking por categoria

```dax
Ranking Categoria HTML =
VAR _tot = [Total Vendido]
VAR _t = ADDCOLUMNS ( VALUES ( vendas[Categoria] ), "@v", [Total Vendido] )
VAR _max = MAXX ( _t, [@v] )
VAR _linhas =
    CONCATENATEX (
        _t,
        VAR _atual = [@v]
        VAR _pos = COUNTROWS ( FILTER ( _t, [@v] > _atual ) ) + 1
        VAR _w = ROUND ( DIVIDE ( [@v], _max ) * 100, 0 ) + 0
        VAR _cor = IF ( [@v] = _max, "#12239E", "#4d7cf0" )
        RETURN
            "<div style='margin-top:20px'>"
                & "<div style='display:flex;justify-content:space-between;font-size:18px'>"
                & "<span style='font-weight:700;color:#1f2a60'>" & _pos & "º &nbsp;" & vendas[Categoria] & "</span>"
                & "<span style='color:#5c6690;font-weight:600'>R$ " & FORMAT ( [@v] / 1000000, "0.0", "pt-BR" ) & " Mi &nbsp;|&nbsp; "
                & FORMAT ( DIVIDE ( [@v], _tot ), "0%", "pt-BR" ) & "</span></div>"
                & "<div style='height:14px;background:#e8ebf5;border-radius:8px;margin-top:8px;overflow:hidden'>"
                & "<div style='height:14px;width:" & _w & "%;background:" & _cor & ";border-radius:8px'></div></div>"
                & "</div>",
        "",
        [@v], DESC
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='font-size:24px;font-weight:700;color:#1f2a60'>Faturamento por categoria</div>"
& "<div style='font-size:16px;color:#8a93b2;margin-top:2px'>Valor e participação no total</div>"
& _linhas
& "</div>"
```
