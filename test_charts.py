#!/usr/bin/env python3
"""Teste de geração de gráficos"""

from tools.data_tools import DataAnalysisTools

def test_visualization():
    print("🧪 Testando geração de gráficos...")
    
    tools = DataAnalysisTools()
    
    # Teste 1: Gráfico de linha simples
    result = tools.create_visualization([1, 2, 3, 4, 5], 'line')
    print(f"✅ Tipo: {type(result)}")
    
    if isinstance(result, str):
        print(f"📏 Tamanho: {len(result)} caracteres")
        print(f"🖼️ É data URL? {result.startswith('data:image/png;base64,')}")
        print(f"📋 Primeiro 50 chars: {result[:50]}")
        
        if result.startswith('data:image/png;base64,'):
            print("✅ Gráfico gerado com sucesso! Data URL válida.")
        else:
            print("❌ Problema na geração do gráfico:")
            print(result)
    else:
        print("❌ Resultado não é string:")
        print(result)

if __name__ == "__main__":
    test_visualization()
