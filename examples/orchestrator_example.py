#!/usr/bin/env python3
"""
Exemplo de uso do Agente Orquestrador
Demonstra como o orquestrador automaticamente seleciona agentes especializados
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator_agent import create_orchestrator_agent

def test_orchestrator():
    """Testa o orquestrador com diferentes tipos de mensagens"""
    
    print("🧠 Testando o Agente Orquestrador")
    print("=" * 50)
    
    try:
        # Criar o orquestrador
        orchestrator = create_orchestrator_agent()
        print("✅ Orquestrador criado com sucesso!")
        print()
        
        # Testes com diferentes tipos de mensagem
        test_messages = [
            "Qual é o preço atual da ação PETR4?",
            "Como está o clima hoje em São Paulo?",
            "Analise este código Python: def hello(): print('world')",
            "Preciso analisar dados de vendas em um CSV",
            "Quais são as últimas notícias sobre inteligência artificial?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"📝 Teste {i}: {message}")
            
            # O orquestrador deve analisar e selecionar automaticamente
            response = orchestrator.run(message)
            
            print(f"🤖 Resposta: {response.content[:200]}...")
            print("-" * 50)
            print()
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_orchestrator()
