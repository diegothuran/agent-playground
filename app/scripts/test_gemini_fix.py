#!/usr/bin/env python3
"""
Teste rápido do backend com configurações corrigidas
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.config.gemini_simple import create_fast_gemini
from agno.agent import Agent

def test_simple_agent():
    """Testa criação de agente simples sem ferramentas."""
    model = create_fast_gemini()
    print(f"✅ Modelo criado: {model.id}")
    
    agent = Agent(
        name="Test Agent",
        role="Simple test agent",
        model=model,
        instructions=["Você é um assistente de teste."]
    )
    
    print(f"✅ Agente criado: {agent.name}")
    return agent

if __name__ == "__main__":
    print("🧪 Testando configuração corrigida...")
    agent = test_simple_agent()
    print("🎉 Teste bem-sucedido!")
