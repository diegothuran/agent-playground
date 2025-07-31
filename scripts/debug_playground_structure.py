#!/usr/bin/env python3
"""Teste simples para entender a estrutura do Agno Playground."""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 Investigando estrutura do Agno Playground")
print("=" * 50)

try:
    from agno.playground import Playground
    from agents.web_agent import create_web_agent
    
    print("🤖 Criando um agente de teste...")
    agent = create_web_agent()
    print(f"✅ Agente criado: {agent.name}")
    
    print("🎮 Testando diferentes formas de criar o playground...")
    
    # Teste 1: Lista de agentes
    print("\n1️⃣ Playground com lista de agentes:")
    try:
        playground1 = Playground(agents=[agent])
        print(f"   ✅ Criado! Tipo: {type(playground1)}")
        print(f"   📊 Agentes: {type(playground1.agents) if hasattr(playground1, 'agents') else 'N/A'}")
        if hasattr(playground1, 'agents'):
            if isinstance(playground1.agents, list):
                print(f"   📋 Lista: {[a.name for a in playground1.agents]}")
            elif isinstance(playground1.agents, dict):
                print(f"   📋 Dict: {list(playground1.agents.keys())}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Dicionário de agentes
    print("\n2️⃣ Playground com dicionário de agentes:")
    try:
        playground2 = Playground(agents={"web": agent})
        print(f"   ✅ Criado! Tipo: {type(playground2)}")
        print(f"   📊 Agentes: {type(playground2.agents) if hasattr(playground2, 'agents') else 'N/A'}")
        if hasattr(playground2, 'agents'):
            if isinstance(playground2.agents, list):
                print(f"   📋 Lista: {[a.name for a in playground2.agents]}")
            elif isinstance(playground2.agents, dict):
                print(f"   📋 Dict: {list(playground2.agents.keys())}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Sem argumentos
    print("\n3️⃣ Playground vazio e depois adicionar agentes:")
    try:
        playground3 = Playground()
        print(f"   ✅ Criado! Tipo: {type(playground3)}")
        print(f"   📊 Agentes iniciais: {type(playground3.agents) if hasattr(playground3, 'agents') else 'N/A'}")
        
        # Tentar adicionar agente
        if hasattr(playground3, 'add_agent'):
            playground3.add_agent(agent)
            print("   ✅ Agente adicionado via add_agent")
        elif hasattr(playground3, 'agents') and isinstance(playground3.agents, dict):
            playground3.agents["web"] = agent
            print("   ✅ Agente adicionado diretamente ao dict")
        elif hasattr(playground3, 'agents') and isinstance(playground3.agents, list):
            playground3.agents.append(agent)
            print("   ✅ Agente adicionado diretamente à lista")
        else:
            print("   ⚠️  Não foi possível adicionar agente")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("\n🎯 Investigação concluída!")
    
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()
