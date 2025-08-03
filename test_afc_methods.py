#!/usr/bin/env python3
"""
Teste de diferentes métodos para configurar AFC
"""

import os
import sys
sys.path.append('/home/diego/Documentos/RA/play')

from dotenv import load_dotenv
load_dotenv()

def test_afc_methods():
    """Testa diferentes métodos para configurar AFC."""
    
    print("=== TESTE MÉTODOS AFC ===")
    
    # Método 1: Variáveis de ambiente tradicionais
    print(f"\n1️⃣ Método: Variáveis de ambiente tradicionais")
    os.environ["GOOGLE_GENAI_MAX_REMOTE_CALLS"] = "3"
    os.environ["GENAI_AFC_MAX_REMOTE_CALLS"] = "3"
    
    try:
        from app.config.gemini_simple import create_ultra_fast_gemini
        model1 = create_ultra_fast_gemini()
        print(f"   ✅ Modelo criado: {model1.id}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Método 2: Configuração via google.generativeai
    print(f"\n2️⃣ Método: Configuração via google.generativeai")
    try:
        import google.generativeai as genai
        
        # Tentar configurar cliente diretamente
        if hasattr(genai, 'configure'):
            # Verificar se há parâmetros relacionados ao AFC
            import inspect
            sig = inspect.signature(genai.configure)
            print(f"   Parâmetros do genai.configure: {list(sig.parameters.keys())}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Método 3: Configuração via agno
    print(f"\n3️⃣ Método: Verificar configuração agno")
    try:
        import agno
        
        # Verificar se há configurações globais
        if hasattr(agno, 'settings') or hasattr(agno, 'config'):
            settings = getattr(agno, 'settings', None) or getattr(agno, 'config', None)
            print(f"   Settings encontradas: {settings}")
        else:
            print(f"   Nenhuma configuração global encontrada no agno")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Método 4: Investigar parâmetros do constructor Gemini
    print(f"\n4️⃣ Método: Parâmetros do constructor Gemini")
    try:
        from agno.models.google import Gemini
        import inspect
        
        sig = inspect.signature(Gemini.__init__)
        params = list(sig.parameters.keys())
        print(f"   Parâmetros do Gemini.__init__:")
        for param in params:
            print(f"     - {param}")
            
        # Verificar se há parâmetros relacionados ao AFC
        afc_params = [p for p in params if 'afc' in p.lower() or 'remote' in p.lower() or 'call' in p.lower()]
        if afc_params:
            print(f"   ✅ Parâmetros AFC encontrados: {afc_params}")
        else:
            print(f"   ❌ Nenhum parâmetro AFC encontrado")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        
    # Método 5: Verificar se há configuração no client_params
    print(f"\n5️⃣ Método: Parâmetros do client")
    try:
        model = create_ultra_fast_gemini()
        
        # Verificar client_params
        if hasattr(model, 'client_params'):
            print(f"   Client params: {model.client_params}")
        
        # Verificar generative_model_kwargs
        if hasattr(model, 'generative_model_kwargs'):
            print(f"   Generative model kwargs: {model.generative_model_kwargs}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_afc_methods()
