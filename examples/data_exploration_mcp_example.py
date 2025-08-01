#!/usr/bin/env python3
"""
Exemplo de uso do MCP de Exploração de Dados no Agno Playground

Este exemplo demonstra como usar o assistente orquestrador para exploração
avançada de dados CSV usando o mcp-server-data-exploration integrado.
"""

import os
import sys
from pathlib import Path
import tempfile
import pandas as pd
import numpy as np

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from agents.orchestrator_agent import create_orchestrator_agent


def create_sample_datasets():
    """Cria datasets de exemplo para demonstração."""
    
    # Dataset 1: Vendas de E-commerce
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
    
    ecommerce_data = {
        'data': dates,
        'vendas': np.random.normal(5000, 1500, len(dates)) + 
                 np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 1000,  # Sazonalidade
        'visitas': np.random.normal(1000, 300, len(dates)),
        'conversao': np.random.normal(0.05, 0.02, len(dates)),
        'categoria': np.random.choice(['Eletrônicos', 'Roupas', 'Casa', 'Livros'], len(dates)),
        'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], len(dates))
    }
    
    df_ecommerce = pd.DataFrame(ecommerce_data)
    df_ecommerce['vendas'] = df_ecommerce['vendas'].clip(lower=0)
    df_ecommerce['visitas'] = df_ecommerce['visitas'].clip(lower=0)
    df_ecommerce['conversao'] = df_ecommerce['conversao'].clip(lower=0, upper=1)
    
    # Dataset 2: Dados Meteorológicos
    weather_data = {
        'data': dates,
        'temperatura': np.random.normal(20, 10, len(dates)) + 
                      np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 15,
        'umidade': np.random.normal(60, 20, len(dates)),
        'precipitacao': np.random.exponential(2, len(dates)),
        'vento_velocidade': np.random.gamma(2, 3, len(dates)),
        'pressao': np.random.normal(1013, 15, len(dates)),
        'cidade': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador'], len(dates))
    }
    
    df_weather = pd.DataFrame(weather_data)
    df_weather['umidade'] = df_weather['umidade'].clip(lower=0, upper=100)
    df_weather['precipitacao'] = df_weather['precipitacao'].clip(lower=0)
    
    # Salvar datasets temporários
    temp_dir = tempfile.mkdtemp()
    
    ecommerce_path = os.path.join(temp_dir, 'ecommerce_vendas.csv')
    weather_path = os.path.join(temp_dir, 'dados_meteorologicos.csv')
    
    df_ecommerce.to_csv(ecommerce_path, index=False)
    df_weather.to_csv(weather_path, index=False)
    
    return {
        'ecommerce': {
            'path': ecommerce_path,
            'description': 'Dados de vendas de e-commerce com sazonalidade',
            'topic': 'Análise de vendas e performance de e-commerce'
        },
        'weather': {
            'path': weather_path,
            'description': 'Dados meteorológicos sintéticos com padrões sazonais',
            'topic': 'Padrões meteorológicos e análise climática'
        }
    }


def main():
    """Exemplo principal de uso da exploração de dados MCP."""
    
    print("🔍 Exemplo: Exploração Avançada de Dados MCP")
    print("=" * 55)
    
    # Criar datasets de exemplo
    print("📊 Criando datasets de exemplo...")
    datasets = create_sample_datasets()
    print("✅ Datasets criados com sucesso!")
    
    # Criar o assistente orquestrador
    print("\n🤖 Criando assistente orquestrador...")
    assistant = create_orchestrator_agent()
    
    # Exemplos de perguntas específicas para exploração de dados
    examples = [
        f"Analise o dataset de vendas em: {datasets['ecommerce']['path']}",
        f"Explore os dados meteorológicos em: {datasets['weather']['path']} focando em padrões de temperatura",
        "Crie visualizações das correlações entre todas as variáveis numéricas",
        "Identifique outliers nos dados e explique possíveis causas",
        "Compare as tendências sazonais entre diferentes regiões/categorias",
        "Execute uma análise estatística completa e forneça insights acionáveis"
    ]
    
    print("\n📋 Exemplos de análises que o sistema pode fazer:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n" + "=" * 55)
    print("💡 O assistente escolherá automaticamente as ferramentas de exploração")
    print("   quando detectar perguntas sobre análise de datasets CSV.")
    
    # Informações sobre os datasets
    print("\n📁 Datasets disponíveis:")
    for name, info in datasets.items():
        print(f"\n🗂️  {name.upper()}:")
        print(f"   📄 Arquivo: {info['path']}")
        print(f"   📝 Descrição: {info['description']}")
        print(f"   🎯 Tópico: {info['topic']}")
    
    # Modo interativo
    print("\n🎯 Modo Interativo (digite 'quit' para sair):")
    print("💡 Dicas:")
    print("  • Use os caminhos dos arquivos CSV criados acima")
    print("  • Peça análises específicas como 'correlações', 'outliers', 'tendências'")
    print("  • Solicite visualizações e gráficos específicos")
    
    while True:
        try:
            question = input("\n❓ Sua pergunta sobre análise de dados: ").strip()
            
            if question.lower() in ['quit', 'exit', 'sair']:
                print("👋 Até logo!")
                break
            
            if not question:
                continue
                
            # Sugestões rápidas
            if question == '1':
                question = f"Analise completamente o dataset de e-commerce: {datasets['ecommerce']['path']}"
            elif question == '2':
                question = f"Explore padrões meteorológicos em: {datasets['weather']['path']}"
            
            print("\n🤖 Assistente (Análise de Dados):")
            print("-" * 40)
            
            # O assistente irá automaticamente usar as ferramentas de exploração
            response = assistant.run(question)
            print(response.content)
            
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    # Limpeza
    print("\n🧹 Limpando arquivos temporários...")
    for dataset in datasets.values():
        if os.path.exists(dataset['path']):
            os.remove(dataset['path'])
    print("✅ Limpeza concluída!")


if __name__ == "__main__":
    main()
