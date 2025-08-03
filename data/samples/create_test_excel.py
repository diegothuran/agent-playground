import pandas as pd

# Criar arquivo Excel de teste
data = {
    'Produto': ['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Impressora'],
    'Categoria': ['Informática', 'Informática', 'Informática', 'Informática', 'Informática'],
    'Preço': [2500.00, 89.90, 299.99, 899.00, 449.99],
    'Vendas_Jan': [45, 156, 78, 32, 25],
    'Vendas_Fev': [52, 142, 85, 28, 31],
    'Vendas_Mar': [38, 178, 92, 35, 29],
    'Estoque': [120, 450, 230, 85, 65]
}

df = pd.DataFrame(data)

# Salvar como Excel
df.to_excel('/home/diego/Documentos/RA/play/vendas_teste.xlsx', index=False, sheet_name='Vendas_Q1')

print("✅ Arquivo Excel de teste criado: vendas_teste.xlsx")
