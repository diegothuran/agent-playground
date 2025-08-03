#!/usr/bin/env python3
"""
Teste final de AFC - fazer requisição real e monitorar logs
"""

import os
import sys
import logging
sys.path.append('/home/diego/Documentos/RA/play')

# Configurar logging para capturar tudo
logging.basicConfig(level=logging.DEBUG)

# Carregar variáveis do .env
from dotenv import load_dotenv
load_dotenv()

# Configurar variáveis de ambiente para AFC
os.environ["GOOGLE_GENAI_MAX_REMOTE_CALLS"] = "3"
os.environ["GENAI_AFC_MAX_REMOTE_CALLS"] = "3"

print(f"🔑 GOOGLE_API_KEY configurada: {bool(os.environ.get('GOOGLE_API_KEY'))}")
print(f"🚀 AFC configurado: max_remote_calls = {os.environ.get('GOOGLE_GENAI_MAX_REMOTE_CALLS')}")

def test_afc_real_request():
    """Faz uma requisição real para testar AFC."""
    
    print("=== TESTE REAL AFC ===")
    
    try:
        from agno.agent import Agent
        from app.config.gemini_simple import create_ultra_fast_gemini
        
        # Criar agente
        agent = Agent(
            name="AFC Test Agent",
            role="Agente de teste para AFC",
            model=create_ultra_fast_gemini(),
            instructions=[
                "Você é um agente de teste.",
                "Responda de forma muito concisa e direta.",
                "Use no máximo 10 palavras."
            ]
        )
        
        print(f"✅ Agente criado com modelo: {agent.model.id}")
        
        # Fazer requisição simples
        print(f"\n🔄 Fazendo requisição...")
        response = agent.run("Responda apenas: AFC teste OK")
        
        print(f"✅ Resposta recebida:")
        print(f"  Content: {response.content}")
        print(f"  Modelo usado: {getattr(response, 'model', 'N/A')}")
        
        # Verificar se há informações sobre function calls
        if hasattr(response, 'function_calls'):
            print(f"  Function calls: {response.function_calls}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_current_backend_logs():
    """Verifica os logs atuais do backend."""
    
    print(f"\n=== LOGS BACKEND ===")
    
    log_file = "/home/diego/Documentos/RA/play/logs/orchestrator.log"
    if os.path.exists(log_file):
        print(f"📄 Últimas linhas do log:")
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-10:]:  # Últimas 10 linhas
                    print(f"  {line.strip()}")
        except Exception as e:
            print(f"❌ Erro ao ler log: {e}")
    else:
        print(f"❌ Log não encontrado: {log_file}")

if __name__ == "__main__":
    success = test_afc_real_request()
    check_current_backend_logs()
    
    if success:
        print(f"\n✅ Teste concluído com sucesso!")
    else:
        print(f"\n❌ Teste falhou!")
