"""
Exemplo de uso do sistema de gráficos
"""

import os
import sys

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.data_tools import DataAnalysisTools

def test_chart_generation():
    """Testa a geração de gráficos automatizados."""
    print("🎨 Testando geração de gráficos para o frontend...")
    
    tools = DataAnalysisTools()
    
    # Dados de exemplo
    vendas = [100, 150, 120, 200, 180, 250, 300]
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul"]
    
    # Teste 1: Gráfico de linha
    print("\n📈 Gerando gráfico de linha...")
    chart_line = tools.create_visualization(vendas, "line")
    
    # Teste 2: Gráfico de barras 
    print("📊 Gerando gráfico de barras...")
    chart_bar = tools.create_visualization(vendas, "bar")
    
    # Teste 3: Histograma
    print("📉 Gerando histograma...")
    chart_hist = tools.create_visualization(vendas, "histogram")
    
    # Verificar resultados
    charts = [chart_line, chart_bar, chart_hist]
    chart_types = ["linha", "barras", "histograma"]
    
    for i, (chart, chart_type) in enumerate(zip(charts, chart_types)):
        print(f"\n🔍 Verificando gráfico de {chart_type}:")
        
        if isinstance(chart, str) and chart.startswith("data:image/png;base64,"):
            print(f"  ✅ Gráfico de {chart_type} gerado com sucesso!")
            print(f"  📏 Tamanho: {len(chart)} chars")
            print(f"  🖼️ Pronto para exibição no frontend")
        else:
            print(f"  ❌ Erro no gráfico de {chart_type}:")
            print(f"  📋 Resultado: {chart[:100]}...")
    
    # Simular resposta do agente com gráfico
    print("\n🤖 Exemplo de resposta do agente com gráfico:")
    print("=" * 50)
    example_response = f"""
Aqui está a análise dos dados de vendas:

📊 **Resumo dos Dados:**
- Total de vendas: {sum(vendas)}
- Média mensal: {sum(vendas)/len(vendas):.1f}
- Melhor mês: {meses[vendas.index(max(vendas))]} ({max(vendas)} vendas)

📈 **Visualização:**

{chart_line}

Como podemos ver no gráfico, há uma tendência crescente nas vendas ao longo dos meses.
"""
    
    print(example_response[:200] + "...")
    print("\n✅ O frontend detectará automaticamente o data:image e exibirá o gráfico!")
    
    return True

if __name__ == "__main__":
    test_chart_generation()
