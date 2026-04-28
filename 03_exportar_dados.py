import sqlite3
import pandas as pd

print("Iniciando pipeline de exportação (Data Lake)...")

# 1. Conecta no banco SQLite
conn = sqlite3.connect('mercado_financeiro.db')

# 2. Extrai as tabelas
df_fato = pd.read_sql_query("SELECT * FROM fato_cotacoes", conn)
df_dim = pd.read_sql_query("SELECT * FROM dim_ativos", conn)

# 3. Salva os arquivos no formato universal (CSV)
df_fato.to_csv('fato_cotacoes.csv', index=False)
df_dim.to_csv('dim_ativos.csv', index=False, encoding='utf-8-sig')

conn.close()
print("Sucesso! Arquivos CSV gerados. Prontos para consumo nativo no Power BI.")