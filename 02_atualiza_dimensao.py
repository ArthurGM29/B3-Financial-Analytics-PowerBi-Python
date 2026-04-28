import pandas as pd
import sqlite3

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

# Atualiza no banco de dados (por garantia)
conn = sqlite3.connect('mercado_financeiro.db')
df_dimensao.to_sql('dim_ativos', conn, if_exists='replace', index=False)
conn.close()

# Salva um arquivo CSV diretamente na pasta do projeto
df_dimensao.to_csv('dim_ativos_atualizada.csv', index=False, encoding='utf-8-sig')

print("SUCESSO! O arquivo 'dim_ativos_atualizada.csv' foi criado na sua pasta.")