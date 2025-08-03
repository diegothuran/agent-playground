#!/usr/bin/env python3
"""
Teste final das configurações AFC com requisição real
"""

import os
import sys
import logging
sys.path.append('/home/diego/Documentos/RA/play')

from dotenv import load_dotenv
load_dotenv()

# Configurar logging para ver AFC
logging.basicConfig(level=logging.INFO)

def test_afc_with_real_request():
    """Testa AFC configurado via client_params com requisição real."""
    
    print("=== TESTE AFC COM REQUISIÇÃO REAL ===")
    
    try:
        from agno.agent import Agent
        from agno.models.google import Gemini
        
        # Criar modelo com AFC via client_params
        model_afc = Gemini(
            id="gemini-2.0-flash-lite",
            temperature=0.1,
            max_output_tokens=1024,
            client_params={
                "max_remote_calls": 3,
                "enable_afc": True,
            },
            generative_model_kwargs={
                "max_remote_calls": 3,
                "enable_afc": True,
            }
        )
        
        print(f"✅ Modelo AFC criado com client_params: {model_afc.client_params}")
        
        # Criar agente
        agent = Agent(
            name="AFC Test Agent",
            role="Teste AFC com client_params",
            model=model_afc,
            instructions=["Responda de forma concisa."]
        )
        
        print(f"🔄 Fazendo requisição com AFC configurado...")
        
        # Fazer requisição e capturar logs
        response = agent.run("Diga apenas 'Teste AFC OK'")
        
        print(f"✅ Resposta recebida: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_comparison():
    """Compara modelo com e sem AFC configurado."""
    
    print(f"\n=== COMPARAÇÃO COM/SEM AFC ===")
    
    try:
        from agno.models.google import Gemini
        
        # Modelo SEM configuração AFC explícita
        model_default = Gemini(
            id="gemini-2.0-flash-lite",
            temperature=0.1
        )
        
        # Modelo COM configuração AFC explícita
        model_afc = Gemini(
            id="gemini-2.0-flash-lite", 
            temperature=0.1,
            client_params={
                "max_remote_calls": 3,
                "enable_afc": True,
            }
        )
        
        print(f"📊 Modelo padrão:")
        print(f"   Client params: {getattr(model_default, 'client_params', 'None')}")
        
        print(f"📊 Modelo AFC:")
        print(f"   Client params: {getattr(model_afc, 'client_params', 'None')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na comparação: {e}")
        return False

if __name__ == "__main__":
    success1 = test_comparison()
    success2 = test_afc_with_real_request()
    
    if success1 and success2:
        print(f"\n✅ Todos os testes foram bem-sucedidos!")
        print(f"✨ Agora vamos atualizar a configuração principal!")
    else:
        print(f"\n❌ Alguns testes falharam.")
