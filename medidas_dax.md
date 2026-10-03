# Medidas DAX | VitrineBR

Todas as medidas usadas nas páginas **Visão Geral** (seções 1 a 8) e **Devoluções** (seções 9 a 15). Os painéis são renderizados com o visual **HTML Content**, a partir de medidas que montam o HTML dinamicamente.

Tabelas usadas: `vendas` (uma linha por venda), `Calendario` (tabela de datas relacionada a `vendas[Data]`) e `previsao_vendas` (previsão gerada em Python).

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

## 5. Evolução do faturamento (12 meses, média e previsão em Python)

As barras tracejadas vêm da tabela `previsao_vendas`, gravada pelo script `02_previsao.py`.

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
VAR _maxPrev = MAXX ( previsao_vendas, previsao_vendas[Faturamento_Previsto] )
VAR _maxG = MAX ( _max, _maxPrev )
VAR _alt = 280
VAR _yMed = ROUND ( DIVIDE ( _med, _maxG ) * _alt, 0 ) + 34
VAR _barras =
    CONCATENATEX (
        _t2,
        VAR _h = ROUND ( DIVIDE ( [@val], _maxG ) * _alt, 0 ) + 0
        VAR _cor =
            IF ( [@val] = _max, "#12239E", IF ( [@val] >= _med, "#4d7cf0", "#b9c8f7" ) )
        RETURN
            "<div style='flex:1;text-align:center'>"
                & "<div style='margin-bottom:6px;position:relative;z-index:2'>"
                & "<span style='font-size:18px;font-weight:700;color:#1f2a60;background:#ffffff;padding:0 6px;border-radius:6px'>"
                & FORMAT ( [@val] / 1000000, "0.0", "pt-BR" ) & "</span></div>"
                & "<div style='height:" & _h & "px;background:" & _cor & ";border-radius:8px 8px 0 0;margin:0 8px'></div>"
                & "<div style='height:26px;line-height:26px;margin-top:8px;font-size:17px;font-weight:700;color:#3d4770;text-transform:uppercase'>"
                & FORMAT ( [@fim], "mmm", "pt-BR" ) & "</div>"
                & "</div>",
        "",
        [Value], ASC
    )
VAR _barrasPrev =
    CONCATENATEX (
        previsao_vendas,
        VAR _v = previsao_vendas[Faturamento_Previsto]
        VAR _h = ROUND ( DIVIDE ( _v, _maxG ) * _alt, 0 ) + 0
        RETURN
            "<div style='flex:1;text-align:center'>"
                & "<div style='margin-bottom:6px;position:relative;z-index:2'>"
                & "<span style='font-size:18px;font-weight:700;color:#0f7a47;background:#ffffff;padding:0 6px;border-radius:6px'>"
                & FORMAT ( _v / 1000000, "0.0", "pt-BR" ) & "</span></div>"
                & "<div style='height:" & _h & "px;background:#e6f6ed;border:2px dashed #0f7a47;border-bottom:none;box-sizing:border-box;border-radius:8px 8px 0 0;margin:0 8px'></div>"
                & "<div style='height:26px;line-height:26px;margin-top:8px;font-size:17px;font-weight:700;color:#0f7a47;text-transform:uppercase'>"
                & FORMAT ( previsao_vendas[Mes], "mmm", "pt-BR" ) & "</div>"
                & "</div>",
        "",
        previsao_vendas[Mes], ASC
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24;box-sizing:border-box'>"
& "<div style='display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center'>"
& "<div><div style='font-size:24px;font-weight:700;color:#1f2a60'>Evolução do faturamento</div>"
& "<div style='font-size:16px;color:#8a93b2;margin-top:2px'>Últimos 12 meses e previsão do próximo trimestre, em R$ milhões</div></div>"
& "<div style='display:flex;gap:10px'>"
& "<div style='font-size:15px;font-weight:600;color:#c0392b;background:#fdeaea;padding:7px 14px;border-radius:20px'>Média: R$ "
& FORMAT ( _med / 1000000, "0.00", "pt-BR" ) & " Mi</div>"
& "<div style='font-size:15px;font-weight:600;color:#0f7a47;background:#e6f6ed;padding:7px 14px;border-radius:20px'>Previsão</div>"
& "</div></div>"
& "<div style='position:relative;display:flex;align-items:flex-end;height:350px;margin-top:14px'>"
& "<div style='position:absolute;left:0;right:0;bottom:" & _yMed & "px;border-top:2px dashed #E85D5D;z-index:1'></div>"
& _barras
& "<div style='align-self:stretch;border-left:2px dashed #c5cbe0;margin:0 6px'></div>"
& _barrasPrev
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
VAR _prev = SUM ( previsao_vendas[Faturamento_Previsto] )
VAR _pIni = MIN ( previsao_vendas[Mes] )
VAR _pFim = EOMONTH ( MAX ( previsao_vendas[Mes] ), 0 )
VAR _erro = MAX ( previsao_vendas[Erro_Medio_Teste] )
VAR _aIni = EDATE ( _pIni, -12 )
VAR _aFim = EOMONTH ( _pFim, -12 )
VAR _anoAnt =
    CALCULATE (
        [Total Vendido],
        REMOVEFILTERS ( Calendario ),
        Calendario[Date] >= _aIni && Calendario[Date] <= _aFim
    )
VAR _varPrev = DIVIDE ( _prev - _anoAnt, _anoAnt )
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

& _box & "#f1f4fc" & _lab & "Canal de venda" & _num & "#12239E'>"
& FORMAT ( _online, "0%", "pt-BR" ) & _txt
& "do faturamento vem do <b>canal online</b>, contra " & FORMAT ( 1 - _online, "0%", "pt-BR" ) & " da loja física.</div></div>"

& _box & "#e6f6ed" & _lab & "Sazonalidade" & _num & "#0f7a47'>+"
& FORMAT ( DIVIDE ( _max, _med ) - 1, "0%", "pt-BR" ) & _txt
& "acima da média em <b>" & FORMAT ( _melhor, "mmm/yyyy", "pt-BR" ) & "</b>, o melhor mês do período.</div></div>"

& _box & "#e6f6ed" & _lab & "Previsão (Python)" & _num & "#0f7a47'>R$ "
& FORMAT ( _prev / 1000000, "0.00", "pt-BR" ) & " Mi" & _txt
& "de <b>" & FORMAT ( _pIni, "mmm", "pt-BR" ) & " a " & FORMAT ( _pFim, "mmm/yyyy", "pt-BR" ) & "</b>, "
& FORMAT ( _varPrev, "+0.0%;-0.0%", "pt-BR" ) & " vs. ano anterior. Erro do modelo no teste: "
& FORMAT ( _erro, "0.0%", "pt-BR" ) & ".</div></div>"

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

# Página Devoluções

## 9. Medidas base de devolução

```dax
Qtd Pedidos = COUNTROWS ( vendas )
```

```dax
Qtd Devolucoes = CALCULATE ( COUNTROWS ( vendas ), vendas[Status] = "Devolvida" )
```

```dax
Taxa Devolucao = DIVIDE ( [Qtd Devolucoes], [Qtd Pedidos] )
```

```dax
Valor Devolvido = CALCULATE ( SUM ( vendas[Valor_Total] ), vendas[Status] = "Devolvida" )
```

```dax
Qtd Canceladas = CALCULATE ( COUNTROWS ( vendas ), vendas[Status] = "Cancelada" )
```

## 10. Cabeçalho e cards

```dax
Cabecalho Dev HTML =
VAR _ini = CALCULATE ( MIN ( vendas[Data] ), REMOVEFILTERS ( Calendario ) )
VAR _fim = CALCULATE ( MAX ( vendas[Data] ), REMOVEFILTERS ( Calendario ) )
RETURN
"<div style='font-family:Segoe UI;background:#12239E;border-radius:18px;padding:22px 30px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 3px 14px #0f1b4d40'>"
& "<div><div style='font-size:32px;font-weight:700;color:#ffffff;letter-spacing:1px'>VitrineBR | Análise de Devoluções</div>"
& "<div style='font-size:17px;color:#ffffffcc;margin-top:4px'>Onde, o quê e por que os pedidos voltam</div></div>"
& "<div style='text-align:right'><div style='font-size:15px;color:#ffffffb3;text-transform:uppercase;letter-spacing:1px'>Período analisado</div>"
& "<div style='font-size:22px;font-weight:700;color:#ffffff;margin-top:2px'>"
& FORMAT ( _ini, "mmm/yyyy", "pt-BR" ) & " a " & FORMAT ( _fim, "mmm/yyyy", "pt-BR" ) & "</div></div>"
& "</div>"
```

```dax
Cards Dev HTML =
VAR _taxa = [Taxa Devolucao]
VAR _qtd = [Qtd Devolucoes]
VAR _valor = [Valor Devolvido]
VAR _ped = [Qtd Pedidos]
VAR _canc = [Qtd Canceladas]
VAR _tMot =
    ADDCOLUMNS (
        FILTER ( VALUES ( vendas[Motivo_Devolucao] ), NOT ISBLANK ( vendas[Motivo_Devolucao] ) ),
        "@q", [Qtd Devolucoes]
    )
VAR _qMot = MAXX ( _tMot, [@q] )
VAR _topMot = MAXX ( FILTER ( _tMot, [@q] = _qMot ), vendas[Motivo_Devolucao] )
VAR _card = "flex:1;border-radius:16px;padding:22px 24px;box-shadow:0 4px 14px #0f1b4d40;background:"
VAR _lab = "<div style='font-size:15px;letter-spacing:1px;text-transform:uppercase;color:#ffffffd9;font-weight:600'>"
VAR _val = "<div style='font-size:44px;font-weight:700;color:#ffffff;margin-top:10px;line-height:1.1'>"
VAR _sub = "<div style='font-size:15px;color:#ffffffcc;margin-top:12px'>"
RETURN
"<div style='display:flex;gap:18px;font-family:Segoe UI;padding:8px'>"
& "<div style='" & _card & "#b36b00'>" & _lab & "Taxa de devolução</div>"
& _val & FORMAT ( _taxa, "0.0%", "pt-BR" ) & "</div>"
& _sub & "dos " & FORMAT ( _ped, "#,0", "pt-BR" ) & " pedidos</div></div>"

& "<div style='" & _card & "#0d1a73'>" & _lab & "Pedidos devolvidos</div>"
& _val & FORMAT ( _qtd, "#,0", "pt-BR" ) & "</div>"
& _sub & "No período analisado</div></div>"

& "<div style='" & _card & "#12239E'>" & _lab & "Valor devolvido</div>"
& _val & "R$ " & FORMAT ( _valor / 1000000, "0.00", "pt-BR" ) & " Mi</div>"
& _sub & "Receita que voltou</div></div>"

& "<div style='" & _card & "#1a36b8'>" & _lab & "Principal motivo</div>"
& "<div style='font-size:28px;font-weight:700;color:#ffffff;margin-top:10px;line-height:1.2'>" & _topMot & "</div>"
& _sub & FORMAT ( DIVIDE ( _qMot, _qtd ), "0%", "pt-BR" ) & " das devoluções</div></div>"

& "<div style='" & _card & "#2450d0'>" & _lab & "Cancelamentos</div>"
& _val & FORMAT ( _canc, "#,0", "pt-BR" ) & "</div>"
& _sub & FORMAT ( DIVIDE ( _canc, _ped ), "0.0%", "pt-BR" ) & " dos pedidos</div></div>"
& "</div>"
```

## 11. Carta de controle (carta p, em SVG)

Taxa mensal de devolução em 24 meses, com linha central e limites de controle em média mais ou menos 3 desvios-padrão. Pontos fora dos limites ficam em vermelho.

```dax
Carta Controle HTML =
VAR _fim = EOMONTH ( MAX ( vendas[Data] ), 0 )
VAR _n = 24
VAR _t1 =
    ADDCOLUMNS ( GENERATESERIES ( 0, _n - 1, 1 ), "@fim", EOMONTH ( _fim, [Value] - ( _n - 1 ) ) )
VAR _t2 =
    ADDCOLUMNS (
        _t1,
        "@ped",
            VAR _f = [@fim]
            VAR _i = EOMONTH ( _f, -1 ) + 1
            RETURN
                CALCULATE ( [Qtd Pedidos], REMOVEFILTERS ( Calendario ), Calendario[Date] >= _i && Calendario[Date] <= _f ),
        "@dev",
            VAR _f = [@fim]
            VAR _i = EOMONTH ( _f, -1 ) + 1
            RETURN
                CALCULATE ( [Qtd Devolucoes], REMOVEFILTERS ( Calendario ), Calendario[Date] >= _i && Calendario[Date] <= _f )
    )
VAR _t3 = ADDCOLUMNS ( _t2, "@tx", DIVIDE ( [@dev], [@ped] ) )
VAR _pbar = DIVIDE ( SUMX ( _t3, [@dev] ), SUMX ( _t3, [@ped] ) )
VAR _nbar = AVERAGEX ( _t3, [@ped] )
VAR _sig = SQRT ( DIVIDE ( _pbar * ( 1 - _pbar ), _nbar ) )
VAR _lsc = _pbar + 3 * _sig
VAR _lic = MAX ( _pbar - 3 * _sig, 0 )
VAR _folga = ( _lsc - _lic ) * 0.22
VAR _topo = MAX ( MAXX ( _t3, [@tx] ), _lsc ) + _folga
VAR _base = MAX ( MIN ( MINX ( _t3, [@tx] ), _lic ) - _folga, 0 )
VAR _faixa = _topo - _base
VAR _yLSC = ROUND ( 330 - DIVIDE ( _lsc - _base, _faixa ) * 300, 0 )
VAR _yLC = ROUND ( 330 - DIVIDE ( _pbar - _base, _faixa ) * 300, 0 )
VAR _yLIC = ROUND ( 330 - DIVIDE ( _lic - _base, _faixa ) * 300, 0 )
VAR _fora = COUNTROWS ( FILTER ( _t3, [@tx] > _lsc || [@tx] < _lic ) ) + 0
VAR _pts =
    CONCATENATEX (
        _t3,
        ROUND ( 70 + [Value] * 1560 / ( _n - 1 ), 0 ) & ","
            & ROUND ( 330 - DIVIDE ( [@tx] - _base, _faixa ) * 300, 0 ),
        " ",
        [Value], ASC
    )
VAR _marcas =
    CONCATENATEX (
        _t3,
        VAR _x = ROUND ( 70 + [Value] * 1560 / ( _n - 1 ), 0 )
        VAR _y = ROUND ( 330 - DIVIDE ( [@tx] - _base, _faixa ) * 300, 0 )
        VAR _cor = IF ( [@tx] > _lsc || [@tx] < _lic, "#d64545", "#12239E" )
        RETURN
            "<circle cx='" & _x & "' cy='" & _y & "' r='9' fill='" & _cor & "' stroke='#ffffff' stroke-width='3' />"
                & "<text x='" & _x & "' y='" & ( _y - 18 ) & "' text-anchor='middle' font-size='17' font-weight='700' fill='#1f2a60'>"
                & FORMAT ( [@tx], "0.0%", "pt-BR" ) & "</text>"
                & "<text x='" & _x & "' y='368' text-anchor='middle' font-size='17' font-weight='700' fill='#3d4770'>"
                & FORMAT ( [@fim], "mmm/yy", "pt-BR" ) & "</text>",
        "",
        [Value], ASC
    )
VAR _veredito =
    IF (
        _fora = 0,
        "<div style='font-size:16px;font-weight:700;color:#0f7a47;background:#e6f6ed;padding:8px 16px;border-radius:20px'>Processo sob controle: nenhum mês fora dos limites</div>",
        "<div style='font-size:16px;font-weight:700;color:#c0392b;background:#fdeaea;padding:8px 16px;border-radius:20px'>" & _fora & " mês(es) fora dos limites de controle</div>"
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center'>"
& "<div><div style='font-size:24px;font-weight:700;color:#1f2a60'>Carta de controle da taxa de devolução</div>"
& "<div style='font-size:16px;color:#8a93b2;margin-top:2px'>Taxa mensal, 24 meses. Limites de controle: média &#177; 3 desvios-padrão (carta p)</div></div>"
& _veredito & "</div>"
& "<svg viewBox='0 0 1800 385' style='width:100%;font-family:Segoe UI;margin-top:10px'>"
& "<rect x='40' y='" & _yLSC & "' width='1620' height='" & ( _yLIC - _yLSC ) & "' fill='#eef2fd' />"
& "<line x1='40' y1='" & _yLSC & "' x2='1660' y2='" & _yLSC & "' stroke='#E85D5D' stroke-width='3' stroke-dasharray='10 7' />"
& "<line x1='40' y1='" & _yLIC & "' x2='1660' y2='" & _yLIC & "' stroke='#E85D5D' stroke-width='3' stroke-dasharray='10 7' />"
& "<line x1='40' y1='" & _yLC & "' x2='1660' y2='" & _yLC & "' stroke='#8a93b2' stroke-width='2' />"
& "<text x='1672' y='" & ( _yLSC + 6 ) & "' font-size='17' font-weight='700' fill='#c0392b'>LSC " & FORMAT ( _lsc, "0.0%", "pt-BR" ) & "</text>"
& "<text x='1672' y='" & ( _yLC + 6 ) & "' font-size='17' font-weight='700' fill='#3d4770'>Média " & FORMAT ( _pbar, "0.0%", "pt-BR" ) & "</text>"
& "<text x='1672' y='" & ( _yLIC + 6 ) & "' font-size='17' font-weight='700' fill='#c0392b'>LIC " & FORMAT ( _lic, "0.0%", "pt-BR" ) & "</text>"
& "<polyline fill='none' stroke='#12239E' stroke-width='4' stroke-linejoin='round' points='" & _pts & "' />"
& _marcas
& "</svg></div>"
```

## 12. Pareto dos motivos

Barras em HTML e linha de percentual acumulado em SVG. As barras escuras são os motivos que somam até 80% das devoluções.

```dax
Pareto Motivos HTML =
VAR _t =
    ADDCOLUMNS (
        FILTER ( VALUES ( vendas[Motivo_Devolucao] ), NOT ISBLANK ( vendas[Motivo_Devolucao] ) ),
        "@q", [Qtd Devolucoes]
    )
VAR _tot = SUMX ( _t, [@q] )
VAR _max = MAXX ( _t, [@q] )
VAR _qtdMot = COUNTROWS ( _t )
VAR _alt = 260
VAR _vitais =
    COUNTROWS (
        FILTER ( _t, VAR _a = [@q] RETURN DIVIDE ( SUMX ( FILTER ( _t, [@q] > _a ), [@q] ), _tot ) + 0 < 0.8 )
    )
VAR _pts =
    CONCATENATEX (
        _t,
        VAR _a = [@q]
        VAR _pos = COUNTROWS ( FILTER ( _t, [@q] > _a ) ) + 1
        VAR _cum = DIVIDE ( SUMX ( FILTER ( _t, [@q] >= _a ), [@q] ), _tot )
        RETURN
            ROUND ( ( _pos - 0.5 ) * 100 / _qtdMot, 0 ) & "," & ROUND ( 100 - _cum * 100, 0 ),
        " ",
        [@q], DESC
    )
VAR _cols =
    CONCATENATEX (
        _t,
        VAR _a = [@q]
        VAR _cumAnt = DIVIDE ( SUMX ( FILTER ( _t, [@q] > _a ), [@q] ), _tot ) + 0
        VAR _cum = DIVIDE ( SUMX ( FILTER ( _t, [@q] >= _a ), [@q] ), _tot )
        VAR _h = ROUND ( DIVIDE ( [@q], _max ) * _alt * 0.7, 0 ) + 0
        VAR _cor = IF ( _cumAnt < 0.8, "#12239E", "#b9c8f7" )
        VAR _yb = ROUND ( _cum * _alt, 0 )
        RETURN
            "<div style='flex:1;text-align:center'>"
                & "<div style='position:relative;height:" & _alt & "px;display:flex;align-items:flex-end;justify-content:center'>"
                & "<div style='width:58%;height:" & _h & "px;background:" & _cor & ";border-radius:8px 8px 0 0'></div>"
                & "<div style='position:absolute;left:50%;bottom:" & _yb & "px;transform:translate(-50%,50%);z-index:2;background:#ffffff;border:2px solid #d98a00;color:#b36b00;font-size:17px;font-weight:700;padding:2px 10px;border-radius:12px'>"
                & FORMAT ( _cum, "0%", "pt-BR" ) & "</div></div>"
                & "<div style='font-size:26px;font-weight:700;color:#1f2a60;margin-top:8px'>" & FORMAT ( [@q], "#,0", "pt-BR" ) & "</div>"
                & "<div style='font-size:18px;font-weight:700;color:#1f2a60;margin-top:2px;line-height:1.25;padding:0 6px'>" & vendas[Motivo_Devolucao] & "</div>"
                & "</div>",
        "",
        [@q], DESC
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='font-size:26px;font-weight:700;color:#1f2a60'>Pareto dos motivos de devolução</div>"
& "<div style='font-size:17px;color:#5c6690;margin-top:2px'>" & _vitais & " de " & _qtdMot & " motivos concentram 80% das devoluções. Linha: percentual acumulado</div>"
& "<div style='position:relative;display:flex;margin-top:36px'>"
& "<svg viewBox='0 0 100 100' preserveAspectRatio='none' style='position:absolute;left:0;top:0;width:100%;height:" & _alt & "px;z-index:1'>"
& "<line x1='0' y1='20' x2='100' y2='20' stroke='#E85D5D' stroke-width='2' stroke-dasharray='6 5' vector-effect='non-scaling-stroke' />"
& "<polyline fill='none' stroke='#d98a00' stroke-width='3' vector-effect='non-scaling-stroke' points='" & _pts & "' /></svg>"
& "<div style='position:absolute;right:0;top:" & ( ROUND ( _alt * 0.2, 0 ) - 26 ) & "px;font-size:16px;font-weight:700;color:#c0392b;z-index:2'>80%</div>"
& _cols
& "</div></div>"
```

## 13. Taxa por categoria, com teste de proporção

Para cada grupo, calcula o z-score da taxa em relação à média geral. Acima de 1,96 a diferença é significativa com 95% de confiança.

```dax
Taxa Categoria HTML =
VAR _geral = [Taxa Devolucao]
VAR _t =
    ADDCOLUMNS (
        VALUES ( vendas[Categoria] ),
        "@tx", [Taxa Devolucao],
        "@q", [Qtd Devolucoes],
        "@n", [Qtd Pedidos]
    )
VAR _max = MAXX ( _t, [@tx] )
VAR _linhas =
    CONCATENATEX (
        _t,
        VAR _atual = [@tx]
        VAR _pos = COUNTROWS ( FILTER ( _t, [@tx] > _atual ) ) + 1
        VAR _w = ROUND ( DIVIDE ( [@tx], _max ) * 100, 0 ) + 0
        VAR _z = DIVIDE ( [@tx] - _geral, SQRT ( DIVIDE ( _geral * ( 1 - _geral ), [@n] ) ) )
        VAR _cor = IF ( _z > 1.96, "#d98a00", IF ( _z < -1.96, "#159a5b", "#4d7cf0" ) )
        VAR _tag = IF ( _z > 1.96, "Acima do esperado", IF ( _z < -1.96, "Abaixo do esperado", "Variação normal" ) )
        VAR _bgTag = IF ( _z > 1.96, "#fdf3e0", IF ( _z < -1.96, "#e6f6ed", "#e8ecfb" ) )
        VAR _corTag = IF ( _z > 1.96, "#b36b00", IF ( _z < -1.96, "#0f7a47", "#3d4770" ) )
        RETURN
            "<div style='margin-top:20px'>"
                & "<div style='display:flex;justify-content:space-between;align-items:center'>"
                & "<span><span style='font-size:21px;font-weight:700;color:#1f2a60'>" & _pos & "º &nbsp;" & vendas[Categoria] & "</span>"
                & "<span style='font-size:15px;font-weight:700;margin-left:12px;padding:4px 12px;border-radius:12px;background:" & _bgTag & ";color:" & _corTag & "'>" & _tag & "</span></span>"
                & "<span><span style='font-size:22px;font-weight:700;color:#1f2a60'>" & FORMAT ( [@tx], "0.0%", "pt-BR" ) & "</span>"
                & "<span style='font-size:17px;font-weight:600;color:#3d4770'> &nbsp;|&nbsp; " & FORMAT ( [@q], "#,0", "pt-BR" ) & " dev. &nbsp;|&nbsp; z = " & FORMAT ( _z, "0.0", "pt-BR" ) & "</span></span></div>"
                & "<div style='height:16px;background:#e8ebf5;border-radius:8px;margin-top:8px;overflow:hidden'>"
                & "<div style='height:16px;width:" & _w & "%;background:" & _cor & ";border-radius:8px'></div></div>"
                & "</div>",
        "",
        [@tx], DESC
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='font-size:26px;font-weight:700;color:#1f2a60'>Taxa de devolução por categoria</div>"
& "<div style='font-size:17px;color:#5c6690;margin-top:2px'>Média geral de " & FORMAT ( _geral, "0.0%", "pt-BR" ) & ". Teste de proporção com 95% de confiança</div>"
& _linhas
& "</div>"
```

## 14. Taxa por região, com teste de proporção

```dax
Taxa Regiao HTML =
VAR _geral = [Taxa Devolucao]
VAR _t =
    ADDCOLUMNS (
        VALUES ( vendas[Regiao] ),
        "@tx", [Taxa Devolucao],
        "@q", [Qtd Devolucoes],
        "@n", [Qtd Pedidos]
    )
VAR _max = MAXX ( _t, [@tx] )
VAR _linhas =
    CONCATENATEX (
        _t,
        VAR _atual = [@tx]
        VAR _pos = COUNTROWS ( FILTER ( _t, [@tx] > _atual ) ) + 1
        VAR _w = ROUND ( DIVIDE ( [@tx], _max ) * 100, 0 ) + 0
        VAR _z = DIVIDE ( [@tx] - _geral, SQRT ( DIVIDE ( _geral * ( 1 - _geral ), [@n] ) ) )
        VAR _cor = IF ( _z > 1.96, "#d98a00", IF ( _z < -1.96, "#159a5b", "#4d7cf0" ) )
        VAR _tag = IF ( _z > 1.96, "Acima do esperado", IF ( _z < -1.96, "Abaixo do esperado", "Variação normal" ) )
        VAR _bgTag = IF ( _z > 1.96, "#fdf3e0", IF ( _z < -1.96, "#e6f6ed", "#e8ecfb" ) )
        VAR _corTag = IF ( _z > 1.96, "#b36b00", IF ( _z < -1.96, "#0f7a47", "#3d4770" ) )
        RETURN
            "<div style='margin-top:20px'>"
                & "<div style='display:flex;justify-content:space-between;align-items:center'>"
                & "<span><span style='font-size:21px;font-weight:700;color:#1f2a60'>" & _pos & "º &nbsp;" & vendas[Regiao] & "</span>"
                & "<span style='font-size:15px;font-weight:700;margin-left:12px;padding:4px 12px;border-radius:12px;background:" & _bgTag & ";color:" & _corTag & "'>" & _tag & "</span></span>"
                & "<span><span style='font-size:22px;font-weight:700;color:#1f2a60'>" & FORMAT ( [@tx], "0.0%", "pt-BR" ) & "</span>"
                & "<span style='font-size:17px;font-weight:600;color:#3d4770'> &nbsp;|&nbsp; " & FORMAT ( [@q], "#,0", "pt-BR" ) & " dev. &nbsp;|&nbsp; z = " & FORMAT ( _z, "0.0", "pt-BR" ) & "</span></span></div>"
                & "<div style='height:16px;background:#e8ebf5;border-radius:8px;margin-top:8px;overflow:hidden'>"
                & "<div style='height:16px;width:" & _w & "%;background:" & _cor & ";border-radius:8px'></div></div>"
                & "</div>",
        "",
        [@tx], DESC
    )
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='font-size:26px;font-weight:700;color:#1f2a60'>Taxa de devolução por região</div>"
& "<div style='font-size:17px;color:#5c6690;margin-top:2px'>Média geral de " & FORMAT ( _geral, "0.0%", "pt-BR" ) & ". Teste de proporção com 95% de confiança</div>"
& _linhas
& "</div>"
```

## 15. Conclusões automáticas

Lê os resultados da carta de controle, dos testes de proporção e do Pareto, e escreve as conclusões.

```dax
Conclusoes Dev HTML =
VAR _geral = [Taxa Devolucao]
VAR _fim = EOMONTH ( MAX ( vendas[Data] ), 0 )
VAR _n = 24
VAR _t1 =
    ADDCOLUMNS ( GENERATESERIES ( 0, _n - 1, 1 ), "@fim", EOMONTH ( _fim, [Value] - ( _n - 1 ) ) )
VAR _t2 =
    ADDCOLUMNS (
        _t1,
        "@ped",
            VAR _f = [@fim]
            VAR _i = EOMONTH ( _f, -1 ) + 1
            RETURN
                CALCULATE ( [Qtd Pedidos], REMOVEFILTERS ( Calendario ), Calendario[Date] >= _i && Calendario[Date] <= _f ),
        "@dev",
            VAR _f = [@fim]
            VAR _i = EOMONTH ( _f, -1 ) + 1
            RETURN
                CALCULATE ( [Qtd Devolucoes], REMOVEFILTERS ( Calendario ), Calendario[Date] >= _i && Calendario[Date] <= _f )
    )
VAR _t3 = ADDCOLUMNS ( _t2, "@tx", DIVIDE ( [@dev], [@ped] ) )
VAR _pbar = DIVIDE ( SUMX ( _t3, [@dev] ), SUMX ( _t3, [@ped] ) )
VAR _sig = SQRT ( DIVIDE ( _pbar * ( 1 - _pbar ), AVERAGEX ( _t3, [@ped] ) ) )
VAR _lsc = _pbar + 3 * _sig
VAR _lic = MAX ( _pbar - 3 * _sig, 0 )
VAR _fora = COUNTROWS ( FILTER ( _t3, [@tx] > _lsc || [@tx] < _lic ) ) + 0
VAR _txMin = MINX ( _t3, [@tx] )
VAR _txMax = MAXX ( _t3, [@tx] )

VAR _tCat =
    ADDCOLUMNS ( VALUES ( vendas[Categoria] ), "@tx", [Taxa Devolucao], "@n", [Qtd Pedidos] )
VAR _tCatZ =
    ADDCOLUMNS ( _tCat, "@z", DIVIDE ( [@tx] - _geral, SQRT ( DIVIDE ( _geral * ( 1 - _geral ), [@n] ) ) ) )
VAR _catSig = FILTER ( _tCatZ, [@z] > 1.96 )
VAR _nCat = COUNTROWS ( _catSig ) + 0
VAR _catNomes = CONCATENATEX ( _catSig, vendas[Categoria], ", ", [@z], DESC )
VAR _catTx = MAXX ( _catSig, [@tx] )

VAR _tReg =
    ADDCOLUMNS ( VALUES ( vendas[Regiao] ), "@tx", [Taxa Devolucao], "@n", [Qtd Pedidos] )
VAR _tRegZ =
    ADDCOLUMNS ( _tReg, "@z", DIVIDE ( [@tx] - _geral, SQRT ( DIVIDE ( _geral * ( 1 - _geral ), [@n] ) ) ) )
VAR _regSig = FILTER ( _tRegZ, [@z] > 1.96 )
VAR _nReg = COUNTROWS ( _regSig ) + 0
VAR _regNomes = CONCATENATEX ( _regSig, vendas[Regiao], ", ", [@z], DESC )
VAR _regTopTx = MAXX ( _tReg, [@tx] )
VAR _regTop = MAXX ( FILTER ( _tReg, [@tx] = _regTopTx ), vendas[Regiao] )

VAR _tMot =
    ADDCOLUMNS (
        FILTER ( VALUES ( vendas[Motivo_Devolucao] ), NOT ISBLANK ( vendas[Motivo_Devolucao] ) ),
        "@q", [Qtd Devolucoes]
    )
VAR _totMot = SUMX ( _tMot, [@q] )
VAR _m1q = MAXX ( _tMot, [@q] )
VAR _m1 = MAXX ( FILTER ( _tMot, [@q] = _m1q ), vendas[Motivo_Devolucao] )
VAR _tMot2 = FILTER ( _tMot, [@q] < _m1q )
VAR _m2q = MAXX ( _tMot2, [@q] )
VAR _m2 = MAXX ( FILTER ( _tMot2, [@q] = _m2q ), vendas[Motivo_Devolucao] )

VAR _box = "<div style='flex:1 1 45%;border-radius:14px;padding:18px 20px;background:"
VAR _lab = "'><div style='font-size:16px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#3d4770'>"
VAR _num = "</div><div style='font-size:32px;font-weight:700;line-height:1.15;margin-top:6px;color:"
VAR _txt = "</div><div style='font-size:18px;font-weight:600;color:#1f2a60;margin-top:8px;line-height:1.4'>"
RETURN
"<div style='font-family:Segoe UI;background:#ffffff;border-radius:18px;padding:24px 28px;box-shadow:0 3px 14px #0f1b4d24'>"
& "<div style='font-size:26px;font-weight:700;color:#1f2a60'>Conclusões da análise</div>"
& "<div style='font-size:17px;color:#5c6690;margin-top:2px'>Geradas automaticamente a partir dos testes estatísticos</div>"
& "<div style='display:flex;flex-wrap:wrap;gap:16px;margin-top:18px'>"

& _box & IF ( _fora = 0, "#e6f6ed", "#fdeaea" ) & _lab & "1. Estabilidade" & _num & IF ( _fora = 0, "#0f7a47", "#c0392b" ) & "'>"
& IF ( _fora = 0, "Processo sob controle", _fora & " mês(es) fora do limite" ) & _txt
& "A taxa mensal variou de " & FORMAT ( _txMin, "0.0%", "pt-BR" ) & " a " & FORMAT ( _txMax, "0.0%", "pt-BR" )
& IF ( _fora = 0, ", sempre dentro dos limites de controle. Não há causa especial a investigar.", ". Investigar o que mudou nos meses fora da faixa." )
& "</div></div>"

& _box & IF ( _nCat > 0, "#fdf3e0", "#f1f4fc" ) & _lab & "2. Onde agir" & _num & IF ( _nCat > 0, "#b36b00", "#12239E" ) & "'>"
& IF ( _nCat > 0, _catNomes, "Nenhuma categoria" ) & _txt
& IF (
    _nCat > 0,
    "tem taxa de até " & FORMAT ( _catTx, "0.0%", "pt-BR" ) & ", acima da média de " & FORMAT ( _geral, "0.0%", "pt-BR" ) & " com significância estatística. É a prioridade.",
    "difere da média de " & FORMAT ( _geral, "0.0%", "pt-BR" ) & " com significância estatística."
)
& "</div></div>"

& _box & IF ( _nReg > 0, "#fdf3e0", "#f1f4fc" ) & _lab & "3. Regiões" & _num & IF ( _nReg > 0, "#b36b00", "#12239E" ) & "'>"
& IF ( _nReg > 0, _regNomes, "Sem diferença real" ) & _txt
& IF (
    _nReg > 0,
    "apresenta taxa acima da média com significância estatística.",
    _regTop & " lidera com " & FORMAT ( _regTopTx, "0.0%", "pt-BR" ) & ", mas a diferença está dentro da variação normal. Não justifica ação regional."
)
& "</div></div>"

& _box & "#f1f4fc" & _lab & "4. Causa principal" & _num & "#12239E'>"
& _m1 & _txt
& "Somado a <b>" & _m2 & "</b>, responde por " & FORMAT ( DIVIDE ( _m1q + _m2q, _totMot ), "0%", "pt-BR" )
& " das devoluções. Atacar esses dois motivos é o caminho de maior retorno."
& "</div></div>"

& "</div></div>"
```
