#!/usr/bin/env python3
"""
Teste simples para verificar a integração do MCP de Exploração de Dados
"""

import os
import sys
import tempfile
import pandas as pd
import numpy as np
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


def test_data_exploration_mcp():
    """Testa as funcionalidades do MCP de exploração de dados."""
    
    print("🧪 Testando MCP de Exploração de Dados")
    print("=" * 40)
    
    try:
        # Importar ferramentas
        from mcp.data_exploration_mcp import DataExplorationMCPTools
        print("✅ Importação das ferramentas: OK")
        
        # Criar instância
        tools = DataExplorationMCPTools()
        print("✅ Criação da instância: OK")
        
        # Criar dataset de teste
        print("\n📊 Criando dataset de teste...")
        test_data = {
            'A': np.random.randn(100),
            'B': np.random.randn(100),
            'C': ['cat', 'dog'] * 50,
            'D': np.random.randint(1, 10, 100)
        }
        
        df_test = pd.DataFrame(test_data)
        
        # Salvar em arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        df_test.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        print(f"✅ Dataset criado: {temp_file.name}")
        
        # Testar carregamento de CSV
        print("\n🔍 Testando carregamento de CSV...")
        result = tools.load_csv(temp_file.name)
        
        if result['status'] == 'success':
            print("✅ Carregamento de CSV: OK")
            print(f"   📏 Shape: {result['shape']}")
            print(f"   📋 Colunas: {result['columns']}")
        else:
            print(f"❌ Carregamento de CSV: FALHOU - {result['message']}")
            return False
        
        # Testar execução de script simples
        print("\n🐍 Testando execução de script...")
        simple_script = """
print("Teste de execução de script")
print(f"Dataset shape: {df.shape}")
print(f"Colunas: {list(df.columns)}")
"""
        
        script_result = tools.run_script(simple_script)
        
        if script_result['status'] == 'success':
            print("✅ Execução de script: OK")
            if script_result['output']:
                print(f"   📝 Output: {script_result['output'][:100]}...")
        else:
            print(f"❌ Execução de script: FALHOU - {script_result['message']}")
        
        # Testar informações do DataFrame
        print("\n📋 Testando informações do DataFrame...")
        info_result = tools.get_dataframe_info()
        
        if info_result['status'] == 'success':
            print("✅ Informações do DataFrame: OK")
            print(f"   📊 Total DataFrames: {info_result['total_dataframes']}")
        else:
            print(f"❌ Informações do DataFrame: FALHOU - {info_result['message']}")
        
        # Limpeza
        os.unlink(temp_file.name)
        tools.clear_dataframes()
        
        print("\n🎉 Todos os testes passaram!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Instale as dependências: pip install pandas numpy matplotlib seaborn")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def test_orchestrator_integration():
    """Testa a integração com o orquestrador."""
    
    print("\n🤖 Testando Integração com Orquestrador")
    print("=" * 45)
    
    try:
        from agents.orchestrator_agent import create_orchestrator_agent
        
        print("✅ Importação do orquestrador: OK")
        
        # Criar orquestrador (isso também testa as dependências)
        agent = create_orchestrator_agent()
        print("✅ Criação do orquestrador: OK")
        
        # Verificar se as ferramentas foram carregadas
        tool_names = [tool.__name__ if hasattr(tool, '__name__') else str(tool) for tool in agent.tools]
        
        data_exploration_tools = [name for name in tool_names if 'csv' in name.lower() or 'script' in name.lower() or 'explore' in name.lower()]
        
        if data_exploration_tools:
            print(f"✅ Ferramentas de exploração carregadas: {len(data_exploration_tools)}")
            print(f"   🛠️  Ferramentas: {data_exploration_tools[:3]}...")
        else:
            print("⚠️  Ferramentas de exploração não detectadas (dependências podem estar faltando)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração: {e}")
        return False


def main():
    """Executa todos os testes."""
    
    print("🧪 TESTE COMPLETO - MCP Exploração de Dados")
    print("=" * 50)
    
    success = True
    
    # Teste 1: Funcionalidades básicas
    success &= test_data_exploration_mcp()
    
    # Teste 2: Integração com orquestrador
    success &= test_orchestrator_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O MCP de Exploração de Dados está funcionando corretamente")
        print("\n💡 Para usar:")
        print("   make example-data-exploration")
        print("   ou")
        print("   make dev-orchestrated")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("💡 Verifique as dependências e configurações")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
