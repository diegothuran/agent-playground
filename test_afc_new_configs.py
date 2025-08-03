"""
Nova configuração Gemini com AFC através de client_params
"""

import os
from agno.models.google import Gemini

def create_afc_optimized_gemini_v2():
    """
    Cria Gemini com AFC otimizado usando client_params e generative_model_kwargs.
    """
    
    # Tentar configurar AFC via client_params
    client_params = {
        "max_remote_calls": 3,
        "enable_afc": True,
    }
    
    # Tentar configurar AFC via generative_model_kwargs
    generative_model_kwargs = {
        "max_remote_calls": 3,
        "enable_afc": True,
    }
    
    return Gemini(
        id="gemini-2.0-flash-lite",
        temperature=0.1,
        max_output_tokens=1024,
        top_p=0.8,
        top_k=20,
        client_params=client_params,
        generative_model_kwargs=generative_model_kwargs
    )

def create_afc_optimized_gemini_v3():
    """
    Cria Gemini com AFC via request_params.
    """
    
    # Tentar configurar AFC via request_params
    request_params = {
        "max_remote_calls": 3,
        "enable_afc": True,
    }
    
    return Gemini(
        id="gemini-2.0-flash-lite",
        temperature=0.1,
        max_output_tokens=1024,
        top_p=0.8,
        top_k=20,
        request_params=request_params
    )

def test_new_afc_configs():
    """Testa as novas configurações de AFC."""
    
    print("=== TESTE NOVAS CONFIGURAÇÕES AFC ===")
    
    configs = [
        ("client_params + generative_model_kwargs", create_afc_optimized_gemini_v2),
        ("request_params", create_afc_optimized_gemini_v3)
    ]
    
    for name, config_func in configs:
        print(f"\n🧪 Testando: {name}")
        try:
            model = config_func()
            print(f"   ✅ Modelo criado: {model.id}")
            print(f"   📋 Client params: {getattr(model, 'client_params', 'N/A')}")
            print(f"   📋 Gen model kwargs: {getattr(model, 'generative_model_kwargs', 'N/A')}")
            print(f"   📋 Request params: {getattr(model, 'request_params', 'N/A')}")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_new_afc_configs()
