# 📊 B3 Financial Analytics: Engenharia de Dados, Riscos e Finanças Quantitativas.

## 1. O Desafio de Negócio (O Problema)

No mercado financeiro, a alocação eficiente de capital exige muito mais do que apenas observar o preço de uma ação. O verdadeiro desafio de um gestor de portfólio é equilibrar a balança entre **Risco (Volatilidade)** e **Retorno**, garantindo que a carteira esteja protegida contra oscilações extremas.

Este projeto End-to-End atua como uma ponte entre a engenharia de dados e a estratégia de investimentos. O objetivo foi construir um pipeline de dados automatizado — desde a extração bruta via API até a visualização em um terminal corporativo — para mapear a eficiência de diferentes setores da economia brasileira e identificar distorções de mercado.

**Perguntas de Negócio respondidas:**

1. Quais empresas e setores entregam o melhor prêmio por risco assumido (Índice Sharpe)?
2. Qual foi o impacto das crises recentes na desvalorização máxima histórica (Drawdown) de cada ativo?
3. Como a alta volatilidade de setores sensíveis (como Varejo) se compara à estabilidade de setores perenes (Energia e Bancos)?
4. Quem são os grandes *outliers* do mercado brasileiro no período analisado?

---

## 2. Arquitetura e Stack Tecnológico

Para garantir escalabilidade, atualização automatizada e performance visual, a solução integrou as seguintes ferramentas:

* **Linguagem de Extração e ETL:** Python (Bibliotecas: `yfinance`, `pandas`, `sqlite3`).
* **SGBD (Data Lake Local):** SQLite.
* **Exportação e Otimização:** Geração de Flat Files (CSV).
* **Modelagem Analítica:** DAX (Data Analysis Expressions).
* **Visualização e UI/UX:** Power BI Desktop.

---

## 3. UI/UX Design e Prototipagem

Um terminal financeiro exige leitura rápida e redução drástica da carga cognitiva. Toda a interface foi pensada para destacar tendências e anomalias sem poluição visual.

* **Dark Mode e Custom Backgrounds:** Utilização de alto contraste para dar destaque aos gráficos de linha e pontos de dispersão, reduzindo o cansaço visual em análises prolongadas.
* **Regra de Proporção 50-25-25:** Redimensionamento estratégico do rodapé, destinando 50% da tela para o gráfico de Risco x Retorno, permitindo a dispersão fluida dos pontos e leitura clara das empresas aglomeradas.
* **Tratamento de Skewness (Distorção):** Remoção de índices como o Ibovespa (Benchmark em pontos) do gráfico de ações (medidas em Reais) para evitar distorção do eixo X e revelar a verdadeira "nuvem" de risco das empresas.
* **Remoção de Ruído:** Supressão de linhas de grade e eixos desnecessários, priorizando rótulos de dados diretos e *Tooltips* personalizados.

---

## 4. Engenharia de Dados (Pipeline em Python)

A arquitetura dispensou bases estáticas. Foi construída uma esteira de dados completa em Python para consumir a API do Yahoo Finance, normalizar os dados com Pandas e estruturar um **Star Schema** diretamente num banco SQLite, exportando posteriormente para CSV visando a máxima performance no Power BI.

<details>
<summary><b>🐍 Script 01: Extração e Carga de Fatos (Clique para expandir)</b></summary>

```python
import yfinance as yf
import pandas as pd
import sqlite3

# Definição do portfólio (17 Ativos Setoriais + 1 Benchmark)
carteira = [
    'ITUB4.SA', 'WEGE3.SA', 'VALE3.SA', 'PETR4.SA', 'RADL3.SA', 
    'BBAS3.SA', 'BBDC4.SA', 'GGBR4.SA', 'SUZB3.SA', 'ABEV3.SA', 
    'LREN3.SA', 'ELET6.SA', 'EQTL3.SA', 'B3SA3.SA', 'MGLU3.SA', 
    'HYPE3.SA', 'RENT3.SA', '^BVSP'
] 

print("Conectando na API do Yahoo Finance e baixando histórico...")

# Extração de dados (2021 a 2026)
dados = yf.download(carteira, start="2021-01-01", end="2026-04-15")['Close']

# Transformação: Unpivot da tabela para o modelo tabular (Tabela Fato)
df_precos = dados.reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Preco_Fechamento')
df_precos.columns = ['Data', 'Ticker', 'Preco_Fechamento']
df_precos['Data'] = df_precos['Data'].dt.strftime('%Y-%m-%d')

# Carga no Banco de Dados SQLite
conn = sqlite3.connect('mercado_financeiro.db')
df_precos.to_sql('fato_cotacoes', conn, if_exists='replace', index=False)
conn.close()

print(f"Extração concluída! {len(df_precos)} registros salvos.")
```
</details>

<details>
<summary><b>🐍 Script 02: Modelagem da Tabela Dimensão (Clique para expandir)</b></summary>

```python
import pandas as pd
import sqlite3

# Estruturação do Catálogo de Ativos com metadados setoriais
dados_dimensao = {
    'Ticker': [
        'ITUB4.SA', 'WEGE3.SA', 'VALE3.SA', 'PETR4.SA', 'RADL3.SA', 
        'BBAS3.SA', 'BBDC4.SA', 'GGBR4.SA', 'SUZB3.SA', 'ABEV3.SA', 
        'LREN3.SA', 'ELET6.SA', 'EQTL3.SA', 'B3SA3.SA', 'MGLU3.SA', 
        'HYPE3.SA', 'RENT3.SA', '^BVSP'
    ],
    'Empresa': [
        'Itaú Unibanco', 'WEG', 'Vale', 'Petrobras', 'Raia Drogasil', 
        'Banco do Brasil', 'Bradesco', 'Gerdau', 'Suzano', 'Ambev', 
        'Lojas Renner', 'Eletrobras', 'Equatorial', 'B3', 'Magalu', 
        'Hypera Pharma', 'Localiza', 'Ibovespa'
    ],
    'Setor': [
        'Financeiro', 'Bens Industriais', 'Materiais Básicos', 'Petróleo e Gás', 'Saúde', 
        'Financeiro', 'Financeiro', 'Materiais Básicos', 'Materiais Básicos', 'Consumo Não Cíclico', 
        'Consumo Cíclico', 'Utilidade Pública', 'Utilidade Pública', 'Financeiro', 'Consumo Cíclico', 
        'Saúde', 'Bens Industriais', 'Benchmark'
    ],
    'Classe_Ativo': [
        'Ação', 'Ação', 'Ação', 'Ação', 'Ação', 
        'Ação', 'Ação', 'Ação', 'Ação', 'Ação', 
        'Ação', 'Ação', 'Ação', 'Ação', 'Ação', 
        'Ação', 'Ação', 'Índice'
    ]
}

df_dimensao = pd.DataFrame(dados_dimensao)

# Carga da Dimensão no Data Lake Local (SQLite)
conn = sqlite3.connect('mercado_financeiro.db')
df_dimensao.to_sql('dim_ativos', conn, if_exists='replace', index=False)
conn.close()

print("Tabela 'dim_ativos' recriada com sucesso!")
```
</details>

<details>
<summary><b>🐍 Script 03: Exportação para Data Lake / CSV (Clique para expandir)</b></summary>

```python
import sqlite3
import pandas as pd

print("Iniciando pipeline de exportação (Data Lake para Power BI)...")

# Conecta no banco SQLite
conn = sqlite3.connect('mercado_financeiro.db')

# Extrai as tabelas formatadas do banco
df_fato = pd.read_sql_query("SELECT * FROM fato_cotacoes", conn)
df_dim = pd.read_sql_query("SELECT * FROM dim_ativos", conn)

# Exportação para Flat Files (CSV Universal) garantindo encoding correto
df_fato.to_csv('fato_cotacoes.csv', index=False)
df_dim.to_csv('dim_ativos.csv', index=False, encoding='utf-8-sig')

conn.close()
print("Sucesso! Arquivos CSV gerados e prontos para consumo no Power BI.")
```
</details>

---

## 5. Desenvolvimento Analítico (Medidas DAX)

Para traduzir a massa de dados brutos em inteligência de negócio, desenvolvi um pacote de métricas financeiras quantitativas utilizando DAX, permitindo a análise de performance sob o contexto de filtros dinâmicos.

```dax
// 1. Preço Final (Cotação mais recente no contexto filtrado)
Preço Final = 
CALCULATE(
    SUM('fato_cotacoes'[Preco_Fechamento]),
    LASTDATE('fato_cotacoes'[Data])
)

// 2. Retorno Acumulado % (Rentabilidade do período)
Retorno Acumulado % = 
VAR Preco_Inicial = CALCULATE(SUM('fato_cotacoes'[Preco_Fechamento]), FIRSTDATE('fato_cotacoes'[Data]))
VAR Preco_Atual = [Preço Final]
RETURN
DIVIDE(Preco_Atual - Preco_Inicial, Preco_Inicial)

// 3. Risco (Volatilidade baseada no Desvio Padrão)
Risco (Volatilidade) = 
STDEV.P('fato_cotacoes'[Preco_Fechamento])

// 4. Índice Sharpe (Métrica de Eficiência Risco x Retorno)
Índice Sharpe = 
ROUND(
    DIVIDE(
        ([Retorno Acumulado %] - 0.13),
        [Risco (Volatilidade)],
        0
    ),
    2
)

// 5. Drawdown Máximo (Análise de Perda Histórica)
Drawdown = 
VAR Pico_Historico = 
    MAXX(
        FILTER(
            ALL('fato_cotacoes'[Data]), 
            'fato_cotacoes'[Data] <= MAX('fato_cotacoes'[Data])
        ), 
        CALCULATE(SUM('fato_cotacoes'[Preco_Fechamento]))
    )
RETURN
DIVIDE([Preço Final] - Pico_Historico, Pico_Historico)
```

---

## 6. Storytelling de Dados e Dashboards

O fluxo do painel foi desenhado para ir do macro (saúde geral) ao micro (detalhe do ativo):

* **Faixa de KPIs (Topo):** Visão imediata do cenário atual (Preço Final, Retorno Acumulado, Risco e Sharpe) responsiva ao contexto da empresa ou setor filtrado.
* **Palco Principal:** Acompanhamento da série temporal (Histórico de Preços) identificando ciclos de alta e baixa do mercado.
* **Rodapé Analítico:**
  * *Risco x Retorno (Dispersão):* Identificação visual de *outliers* (ex: Petrobras com alto retorno; Magalu com alta volatilidade).
  * *Drawdown:* Análise de perda, mapeando o "fundo do poço" histórico para gestão de risco.
  * *Ranking de Sharpe:* Classificação barra a barra das empresas mais eficientes na gestão do capital do acionista.

---

## 7. Conclusão e Plano de Ação

As recomendações estratégicas baseadas na leitura dos dados são:

* **Hedge Setorial:** O portfólio ideal deve equilibrar ativos de *Consumo Cíclico* (alta volatilidade, sensíveis a juros) com empresas de *Utilidade Pública e Financeiro* (baixo risco, garantindo sustentação na base do gráfico de dispersão).
* **Alocação Focada em Sharpe:** Reduzir a exposição a ativos que apresentam alto retorno absoluto, mas com desvio padrão desproporcional, priorizando os líderes do Ranking de Eficiência.
* **Monitoramento de Outliers:** Isolar casos como o da Petrobras para entender se o retorno descolado do mercado é estrutural ou fruto de um evento pontual.

---

## Contato

| 👨‍💻 Autor | **Arthur Mesquita** |
| :--- | :--- |
| **Cargo** | Analista de Dados & BI |
| **LinkedIn** | [linkedin.com/in/arthur-g-mesquita](https://www.linkedin.com/in/arthur-g-mesquita) |
| **Localização** | 📍 Recife, PE |
