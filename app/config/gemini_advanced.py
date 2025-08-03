"""
Configuração avançada para controlar AFC do Gemini
"""

import os
from typing import Any, Dict
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

def configure_afc_globally():
    """
    Tenta configurar AFC globalmente através de diferentes métodos.
    """
    
    # Método 1: Variáveis de ambiente específicas do google-genai
    os.environ["GOOGLE_GENAI_AFC_MAX_REMOTE_CALLS"] = "3"
    os.environ["GENAI_AFC_MAX_REMOTE_CALLS"] = "3"
    
    # Método 2: Configuração através do cliente google.genai
    try:
        import google.genai as genai
        
        # Tentar configurar globalmente se disponível
        if hasattr(genai, 'configure'):
            genai.configure(
                api_key=os.getenv("GOOGLE_API_KEY"),
            )
        
        # Configuração de AFC se disponível
        if hasattr(genai, 'set_afc_config'):
            genai.set_afc_config(max_remote_calls=3)
            
    except Exception as e:
        print(f"Configuração google.genai não disponível: {e}")
    
    # Método 3: Monkey patch para controlar AFC
    try:
        import google.genai.models
        
        # Se houver uma classe ou função específica para AFC, configurar aqui
        original_afc_config = getattr(google.genai.models, '_afc_config', {})
        setattr(google.genai.models, '_afc_config', {
            **original_afc_config,
            'max_remote_calls': 3
        })
        
    except Exception as e:
        print(f"Monkey patch não aplicado: {e}")

def create_afc_optimized_gemini():
    """
    Cria Gemini com configuração AFC otimizada.
    """
    from agno.models.google import Gemini
    
    # Configurar AFC antes de criar o modelo
    configure_afc_globally()
    
    # Tentar diferentes abordagens para passar configurações AFC
    config_attempts = [
        # Tentativa 1: generative_model_kwargs
        {
            "id": "gemini-2.0-flash-lite",
            "temperature": 0.3,
            "max_output_tokens": 2048,
            "generative_model_kwargs": {"max_remote_calls": 3}
        },
        # Tentativa 2: client_params
        {
            "id": "gemini-2.0-flash-lite", 
            "temperature": 0.3,
            "max_output_tokens": 2048,
            "client_params": {"max_remote_calls": 3}
        },
        # Tentativa 3: request_params
        {
            "id": "gemini-2.0-flash-lite",
            "temperature": 0.3, 
            "max_output_tokens": 2048,
            "request_params": {"max_remote_calls": 3}
        },
        # Tentativa 4: básico (fallback)
        {
            "id": "gemini-2.0-flash-lite",
            "temperature": 0.3,
            "max_output_tokens": 2048,
        }
    ]
    
    for i, config in enumerate(config_attempts):
        try:
            model = Gemini(**config)
            print(f"✅ Configuração {i+1} funcionou")
            return model
        except Exception as e:
            print(f"⚠️  Configuração {i+1} falhou: {e}")
            continue
    
    # Se todas falharam, usar configuração básica
    from .gemini_simple import create_ultra_fast_gemini
    return create_ultra_fast_gemini()

# Executar configuração na importação
configure_afc_globally()
