"""
Configuração simples e funcional para Gemini com foco em latência
"""

import os
from agno.models.google import Gemini

def create_fast_gemini():
    """
    Cria Gemini otimizado para latência usando apenas parâmetros suportados.
    AFC será controlado via variáveis de ambiente.
    """
    
    return Gemini(
        id="gemini-2.0-flash-lite",  # Modelo mais rápido
        temperature=0.3,             # Respostas mais diretas
        max_output_tokens=2048,      # Limite balanceado
        top_p=0.8,                   # Configuração para velocidade
        top_k=20                     # Limita escolhas para mais velocidade
    )

def create_simple_gemini():
    """
    Cria Gemini com configuração mínima para máxima compatibilidade.
    """
    return Gemini(
        id="gemini-2.0-flash-lite",
        temperature=0.3
    )

# Para configurar AFC via variáveis de ambiente
def setup_afc_environment():
    """
    Configura variáveis de ambiente para otimizar AFC.
    """
    os.environ.setdefault("GOOGLE_GENAI_MAX_REMOTE_CALLS", "3")
    os.environ.setdefault("GENAI_AFC_MAX_REMOTE_CALLS", "3")

def create_ultra_fast_gemini():
    """
    Cria Gemini otimizado para latência e processamento direto.
    """
    return Gemini(
        id="gemini-2.0-flash-lite",  # Modelo mais rápido disponível
        temperature=0.01,            # EXTREMAMENTE baixa para respostas diretas
        max_output_tokens=600,       # Ainda mais reduzido para velocidade
        top_p=0.6,                   # Muito determinístico
        top_k=10,                    # Muito limitado para velocidade máxima
    )
    
# Executar na importação para aplicar configurações
setup_afc_environment()
