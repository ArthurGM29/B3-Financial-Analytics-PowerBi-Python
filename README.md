# B3 Financial Analytics: Engenharia de Dados, Finanças Quantitativas e UI/UX

## 1. O Desafio de Negócio (O Problema)

No mercado financeiro, a alocação eficiente de capital exige muito mais do que apenas observar o preço de uma ação. O verdadeiro desafio de um gestor de portfólio é equilibrar a balança entre **Risco (Volatilidade)** e **Retorno**, garantindo que a carteira esteja protegida contra oscilações extremas.

Este projeto End-to-End atua como uma ponte entre a engenharia de dados e a estratégia de investimentos. O objetivo foi construir um pipeline de dados automatizado — desde a extração bruta via API até a visualização em um terminal corporativo — para mapear a eficiência de diferentes setores da economia brasileira e identificar distorções de mercado.

**Perguntas de Negócio respondidas:**

1. Quais empresas e setores entregam o melhor prêmio por risco assumido (Índice Sharpe)?
2. Qual foi o impacto das crises recentes na desvalorização máxima histórica (Drawdown) de cada ativo?
3. Como a alta volatilidade de setores sensíveis (como Varejo) se compara à estabilidade de setores perenes (Energia e Bancos)?
4. Quem são os grandes *outliers* do mercado brasileiro no período analisado?

## 2. Arquitetura e Stack Tecnológico

Para garantir escalabilidade, atualização automatizada e performance visual, a solução integrou as seguintes ferramentas:

* **Linguagem de Extração e ETL:** Python (Bibliotecas: `yfinance`, `pandas`).
* **SGBD (Data Lake Local):** SQLite.
* **Exportação e Otimização:** Geração de Flat Files (CSV).
* **Modelagem Analítica:** DAX (Data Analysis Expressions).
* **Visualização e UI/UX:** Power BI Desktop.

## 3. UI/UX Design e Prototipagem

Um terminal financeiro exige leitura rápida e redução drástica da carga cognitiva. Toda a interface foi pensada para destacar tendências e anomalias sem poluição visual.

* **Dark Mode e Custom Backgrounds:** Utilização de alto contraste para dar destaque aos gráficos de linha e pontos de dispersão, reduzindo o cansaço visual em análises prolongadas.
* **Regra de Proporção 50-25-25:** Redimensionamento estratégico do rodapé, destinando 50% da tela para o gráfico de Risco x Retorno, permitindo a dispersão fluida dos pontos e leitura clara das empresas aglomeradas.
* **Tratamento de Skewness (Distorção):** Remoção de índices como o Ibovespa (Benchmark em pontos) do gráfico de ações (medidas em Reais) para evitar distorção do eixo X e revelar a verdadeira "nuvem" de risco das empresas.
* **Remoção de Ruído:** Supressão de linhas de grade e eixos desnecessários, priorizando rótulos de dados diretos.

## 4. Engenharia de Dados e Modelagem (Python & SQLite)

A arquitetura dispensou bases estáticas. Foi construído um script Python para consumir a API do Yahoo Finance, normalizar os dados com Pandas e estruturar um **Star Schema** diretamente em um banco SQLite.

**Script de ETL e Estruturação de Dimensões (Python)**

```python
import pandas as pd
import sqlite3

# 1. Estruturação do Catálogo de Ativos (Tabela Dimensão)
dados_dimensao = {
    'Ticker': ['ITUB4.SA', 'PETR4.SA', 'ELET6.SA', 'MGLU3.SA', '^BVSP'],
    'Empresa': ['Itaú Unibanco', 'Petrobras', 'Eletrobras', 'Magalu', 'Ibovespa'],
    'Setor': ['Financeiro', 'Petróleo e Gás', 'Utilidade Pública', 'Consumo Cíclico', 'Benchmark'],
    'Classe_Ativo': ['Ação', 'Ação', 'Ação', 'Ação', 'Índice']
}

df_dimensao = pd.DataFrame(dados_dimensao)

# 2. Carga no Data Lake Local (SQLite)
conn = sqlite3.connect('mercado_financeiro.db')
df_dimensao.to_sql('dim_ativos', conn, if_exists='replace', index=False)

# 3. Exportação para Flat File (Performance no Power BI)
df_dimensao.to_csv('dim_ativos.csv', index=False, encoding='utf-8-sig')
conn.close()
5. Desenvolvimento Analítico (DAX)Desenvolvi métricas estatísticas e financeiras avançadas para traduzir o histórico de preços em KPIs de tomada de decisão.Principais Medidas de Negócio (DAX)Snippet de código// 1. Cálculo de Volatilidade (Risco)
Risco (Volatilidade) = 
STDEV.P('fato_cotacoes'[Preco_Fechamento])

// 2. Retorno Acumulado do Período
Retorno Acumulado % = 
VAR Preco_Inicial = CALCULATE(MIN('fato_cotacoes'[Preco_Fechamento]), FIRSTDATE('fato_cotacoes'[Data]))
VAR Preco_Final = CALCULATE(MAX('fato_cotacoes'[Preco_Fechamento]), LASTDATE('fato_cotacoes'[Data]))
RETURN
DIVIDE(Preco_Final - Preco_Inicial, Preco_Inicial)

// 3. Índice Sharpe (Eficiência Risco-Retorno)
Índice Sharpe = 
VAR Taxa_Livre_Risco = 0.10 // Selic Base de Exemplo
RETURN
DIVIDE([Retorno Acumulado %] - Taxa_Livre_Risco, [Risco (Volatilidade)])
6. Storytelling de Dados e DashboardsO fluxo do painel foi desenhado para ir do macro (saúde geral) ao micro (detalhe do ativo):Faixa de KPIs (Topo): Visão imediata do cenário atual (Preço Final, Retorno Acumulado, Risco e Sharpe) responsiva ao contexto da empresa ou setor filtrado.Palco Principal: Acompanhamento da série temporal (Histórico de Preços) identificando ciclos de alta e baixa do mercado.Rodapé Analítico:Risco x Retorno (Dispersão): Identificação visual de outliers (ex: Petrobras com alto retorno; Magalu com alta volatilidade).Drawdown: Análise de perda, mapeando o "fundo do poço" histórico para gestão de risco.Ranking de Sharpe: Classificação barra a barra das empresas mais eficientes na gestão do capital do acionista.7. Conclusão e Plano de AçãoAs recomendações estratégicas baseadas na leitura dos dados são:Hedge Setorial: O portfólio ideal deve equilibrar ativos de Consumo Cíclico (alta volatilidade, sensíveis a juros) com empresas de Utilidade Pública e Financeiro (baixo risco, garantindo sustentação na base do gráfico de dispersão).Alocação Focada em Sharpe: Reduzir a exposição a ativos que apresentam alto retorno absoluto, mas com desvio padrão desproporcional, priorizando os líderes do Ranking de Eficiência.Monitoramento de Outliers: Isolar casos como o da Petrobras para entender se o retorno descolado do mercado é estrutural ou fruto de um evento pontual.Contato👨‍💻 AutorArthur MesquitaCargoAnalista de Dados & BILinkedInlinkedin.com/in/arthur-g-mesquitaLocalização📍 Recife, PE
