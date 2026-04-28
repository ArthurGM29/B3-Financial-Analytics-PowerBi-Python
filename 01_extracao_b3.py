import yfinance as yf
import pandas as pd
import sqlite3

# Definindo a carteira de ativos (Tickers da B3 precisam do .SA no final)
# ^BVSP é o código para o índice Ibovespa (Benchmark)
carteira = [
    'ITUB4.SA', 'WEGE3.SA', 'VALE3.SA', 'PETR4.SA', 'RADL3.SA', 
    'BBAS3.SA', 'BBDC4.SA', 'GGBR4.SA', 'SUZB3.SA', 'ABEV3.SA', 
    'LREN3.SA', 'ELET3.SA', 'EQTL3.SA', 'B3SA3.SA', 'MGLU3.SA', 
    'HYPE3.SA', 'RENT3.SA', '^BVSP'
]

print("Conectando na API do Yahoo Finance e baixando histórico...")

dados = yf.download(carteira, start="2021-01-01", end="2026-04-15")['Close']

# Arrumando o formato da tabela para o banco de dados (Unpivot)
df_precos = dados.reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Preco_Fechamento')
df_precos.columns = ['Data', 'Ticker', 'Preco_Fechamento']
df_precos['Data'] = df_precos['Data'].dt.strftime('%Y-%m-%d')

# Salvando em um banco de dados local
conn = sqlite3.connect('mercado_financeiro.db')
df_precos.to_sql('fato_cotacoes', conn, if_exists='replace', index=False)
conn.close()

print(f"Extração concluída! Foram salvos {len(df_precos)} registros no banco de dados.")