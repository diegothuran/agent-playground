#!/usr/bin/env python3
"""
Investigação detalhada sobre AFC no agno/google-genai
"""

import os
import sys
sys.path.append('/home/diego/Documentos/RA/play')

# Configurar variáveis de ambiente
os.environ["GOOGLE_GENAI_MAX_REMOTE_CALLS"] = "3"
os.environ["GENAI_AFC_MAX_REMOTE_CALLS"] = "3"

def investigate_afc():
    """Investiga como o AFC é configurado na biblioteca agno."""
    
    print("=== INVESTIGAÇÃO AFC ===")
    
    try:
        # Importar módulos relevantes
        import agno
        from agno.models.google import Gemini
        import google.generativeai as genai
        
        print(f"✅ Módulos importados:")
        print(f"  - agno version: {getattr(agno, '__version__', 'N/A')}")
        print(f"  - genai available: {genai is not None}")
        
        # Verificar se há configurações globais
        if hasattr(genai, 'configure'):
            print(f"  - genai.configure disponível")
            
        # Verificar configurações no genai
        try:
            config = genai._client._client_config if hasattr(genai, '_client') else None
            print(f"  - Client config: {config}")
        except:
            print(f"  - Não foi possível acessar client config")
            
        # Verificar variáveis de ambiente conhecidas
        afc_vars = [
            "GOOGLE_GENAI_MAX_REMOTE_CALLS",
            "GENAI_AFC_MAX_REMOTE_CALLS", 
            "ANTHROPIC_FUNCTION_CALLING_MAX_REMOTE_CALLS",
            "GOOGLE_GENAI_USE_AFC",
            "GENAI_USE_AFC"
        ]
        
        print(f"\n📋 Variáveis de ambiente AFC:")
        for var in afc_vars:
            value = os.environ.get(var)
            print(f"  - {var}: {value}")
            
    except Exception as e:
        print(f"❌ Erro na investigação: {e}")
        import traceback
        traceback.print_exc()

def check_agno_source():
    """Verifica se conseguimos acessar o código fonte do agno."""
    
    print("\n=== VERIFICAÇÃO CÓDIGO AGNO ===")
    
    try:
        from agno.models.google.gemini import Gemini
        import inspect
        
        # Verificar código fonte do método __init__
        source = inspect.getsource(Gemini.__init__)
        print(f"📄 Código do __init__:")
        lines = source.split('\n')
        for i, line in enumerate(lines[:20]):  # Primeiras 20 linhas
            print(f"  {i+1:2}: {line}")
            
        if len(lines) > 20:
            print(f"  ... ({len(lines)-20} linhas restantes)")
            
    except Exception as e:
        print(f"❌ Erro ao acessar código fonte: {e}")

def test_afc_with_agent():
    """Testa AFC usando um agente real."""
    
    print("\n=== TESTE AFC COM AGENTE ===")
    
    try:
        from agno.agent import Agent
        from app.config.gemini_simple import create_ultra_fast_gemini
        
        # Criar agente simples
        agent = Agent(
            name="Test Agent",
            role="Teste",
            model=create_ultra_fast_gemini(),
            instructions=["Responda de forma concisa."]
        )
        
        print(f"✅ Agente criado:")
        print(f"  - Nome: {agent.name}")
        print(f"  - Modelo: {agent.model.id}")
        
        # Tentar fazer uma requisição
        # response = agent.run("Diga apenas 'AFC funcionando' se você recebeu esta mensagem.")
        # print(f"✅ Resposta: {response}")
        
    except Exception as e:
        print(f"❌ Erro no teste com agente: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigate_afc()
    check_agno_source()
    test_afc_with_agent()
