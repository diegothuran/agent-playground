#!/usr/bin/env python3
"""Teste rápido de criação dos agentes."""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🧪 Teste Rápido dos Agentes")
print("=" * 30)

def test_agents():
    """Testa criação de todos os agentes."""
    agents_tests = [
        ("Web Agent", "agents.web_agent", "create_web_agent"),
        ("Finance Agent", "agents.finance_agent", "create_finance_agent"),
        ("Code Agent", "agents.code_agent", "create_code_agent"),
        ("Data Agent", "agents.data_agent", "create_data_agent"),
        ("MCP Agent", "agents.mcp_agent", "create_mcp_agent")
    ]
    
    created_agents = []
    
    for name, module, func in agents_tests:
        try:
            print(f"🤖 Criando {name}...")
            mod = __import__(module, fromlist=[func])
            create_func = getattr(mod, func)
            agent = create_func()
            created_agents.append(agent)
            print(f"  ✅ {agent.name} - {len(agent.tools)} ferramentas")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
    
    print(f"\n📊 Resultado: {len(created_agents)}/5 agentes criados")
    return created_agents

def test_playground_quick():
    """Teste rápido do playground."""
    try:
        from agno.playground import Playground
        agents = test_agents()
        
        if len(agents) > 0:
            print(f"\n🎮 Criando playground com {len(agents)} agentes...")
            playground = Playground(agents=agents)
            print("✅ Playground criado com sucesso!")
            print(f"📋 Agentes no playground: {[a.name for a in playground.agents]}")
            return True
        else:
            print("\n❌ Nenhum agente foi criado")
            return False
    except Exception as e:
        print(f"\n❌ Erro no playground: {e}")
        return False

if __name__ == "__main__":
    success = test_playground_quick()
    print(f"\n🎯 Resultado final: {'✅ SUCESSO' if success else '❌ FALHOU'}")
    sys.exit(0 if success else 1)
