"""
Configuração ultra-otimizada para Gemini com foco em latência mínima
"""

import os
import asyncio
from agno.models.google import Gemini

def create_ultra_fast_gemini():
    """
    Cria Gemini otimizado para latência MÍNIMA.
    Configurações extremas para velocidade máxima.
    """
    
    # Configurar variáveis de ambiente para máxima velocidade
    os.environ.setdefault("GOOGLE_GENAI_MAX_REMOTE_CALLS", "1")  # Reduzido para 1
    os.environ.setdefault("GENAI_AFC_MAX_REMOTE_CALLS", "1")     # Reduzido para 1
    os.environ.setdefault("GOOGLE_GENAI_TIMEOUT", "10")         # Timeout mais baixo
    
    return Gemini(
        id="gemini-2.0-flash-lite",  # Modelo mais rápido
        temperature=0.01,            # Extremamente baixa para respostas diretas
        max_output_tokens=400,       # Muito reduzido para velocidade
        top_p=0.5,                   # Muito determinístico
        top_k=5,                     # Extremamente limitado
    )

def create_speed_optimized_gemini():
    """
    Versão balanceada entre velocidade e qualidade.
    """
    
    os.environ.setdefault("GOOGLE_GENAI_MAX_REMOTE_CALLS", "2")
    os.environ.setdefault("GENAI_AFC_MAX_REMOTE_CALLS", "2")
    os.environ.setdefault("GOOGLE_GENAI_TIMEOUT", "15")
    
    return Gemini(
        id="gemini-2.0-flash-lite",
        temperature=0.05,
        max_output_tokens=800,
        top_p=0.7,
        top_k=10,
    )

def create_streaming_gemini():
    """
    Configuração otimizada para streaming de respostas.
    """
    
    os.environ.setdefault("GOOGLE_GENAI_STREAM", "true")
    os.environ.setdefault("GOOGLE_GENAI_MAX_REMOTE_CALLS", "1")
    
    return Gemini(
        id="gemini-2.0-flash-lite",
        temperature=0.1,
        max_output_tokens=600,
        top_p=0.8,
        top_k=15,
    )

def setup_performance_environment():
    """
    Configura variáveis de ambiente para máxima performance.
    """
    # Configurações de timeout e concorrência
    os.environ.setdefault("GOOGLE_GENAI_TIMEOUT", "10")
    os.environ.setdefault("GOOGLE_GENAI_MAX_RETRIES", "1")
    os.environ.setdefault("GOOGLE_GENAI_RETRY_DELAY", "0.5")
    
    # Configurações de cache
    os.environ.setdefault("GOOGLE_GENAI_CACHE_TTL", "300")  # 5 minutos
    os.environ.setdefault("GOOGLE_GENAI_ENABLE_CACHE", "true")
    
    # Configurações de AFC
    os.environ.setdefault("GENAI_AFC_MAX_REMOTE_CALLS", "1")
    os.environ.setdefault("GENAI_AFC_TIMEOUT", "8")
    
    # Configurações de threading
    os.environ.setdefault("GOOGLE_GENAI_MAX_WORKERS", "4")
    
def create_cached_gemini():
    """
    Cria Gemini com cache agressivo para respostas repetidas.
    """
    
    setup_performance_environment()
    
    return Gemini(
        id="gemini-2.0-flash-lite",
        temperature=0.0,  # Zero para máximo cache hit
        max_output_tokens=500,
        top_p=0.9,
        top_k=20,
    )

# Aplicar configurações na importação
setup_performance_environment()

# Configuração padrão para uso geral
def get_default_fast_model():
    """Retorna o modelo padrão otimizado."""
    return create_ultra_fast_gemini()

