#!/usr/bin/env python3
"""
Teste para verificar configuração real do Gemini
"""

import os
import sys
sys.path.append('/home/diego/Documentos/RA/play')

# Configurar variáveis de ambiente antes de qualquer importação
os.environ["GOOGLE_GENAI_MAX_REMOTE_CALLS"] = "3"
os.environ["GENAI_AFC_MAX_REMOTE_CALLS"] = "3"
os.environ["ANTHROPIC_FUNCTION_CALLING_MAX_REMOTE_CALLS"] = "3"

from app.config.gemini_simple import create_ultra_fast_gemini

def test_gemini_config():
    """Testa a configuração real do Gemini."""
    
    print("=== TESTE DE CONFIGURAÇÃO GEMINI ===")
    print(f"Variáveis de ambiente:")
    print(f"GOOGLE_GENAI_MAX_REMOTE_CALLS: {os.environ.get('GOOGLE_GENAI_MAX_REMOTE_CALLS')}")
    print(f"GENAI_AFC_MAX_REMOTE_CALLS: {os.environ.get('GENAI_AFC_MAX_REMOTE_CALLS')}")
    
    try:
        # Criar instância do modelo
        model = create_ultra_fast_gemini()
        print(f"\n✅ Modelo criado com sucesso:")
        print(f"  - ID: {getattr(model, 'id', 'N/A')}")
        print(f"  - Temperature: {getattr(model, 'temperature', 'N/A')}")
        print(f"  - Max tokens: {getattr(model, 'max_output_tokens', 'N/A')}")
        
        # Verificar todos os atributos disponíveis
        print(f"\n📋 Atributos do modelo:")
        for attr in dir(model):
            if not attr.startswith('_') and not callable(getattr(model, attr)):
                value = getattr(model, attr)
                print(f"  - {attr}: {value}")
        
        # Tentar verificar configuração interna
        if hasattr(model, '_client'):
            print(f"\n🔍 Cliente interno encontrado:")
            client = getattr(model, '_client')
            for attr in dir(client):
                if 'afc' in attr.lower() or 'remote' in attr.lower():
                    print(f"  - {attr}: {getattr(client, attr, 'N/A')}")
                    
        return model
        
    except Exception as e:
        print(f"❌ Erro ao criar modelo: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_simple_request():
    """Testa uma requisição simples."""
    
    print("\n=== TESTE DE REQUISIÇÃO ===")
    model = create_ultra_fast_gemini()
    
    if model:
        try:
            # Verificar métodos disponíveis
            print(f"Métodos disponíveis:")
            methods = [method for method in dir(model) if not method.startswith('_') and callable(getattr(model, method))]
            for method in methods[:10]:  # Mostra só os primeiros 10
                print(f"  - {method}")
            
            # Tentar o método correto
            if hasattr(model, 'run'):
                response = model.run("Responda apenas 'OK' se você está funcionando.")
                print(f"✅ Resposta recebida: {response}")
            elif hasattr(model, 'invoke'):
                response = model.invoke("Responda apenas 'OK' se você está funcionando.")
                print(f"✅ Resposta recebida: {response}")
            else:
                print("❌ Não encontrei método para fazer requisição")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_gemini_config()
    test_simple_request()
