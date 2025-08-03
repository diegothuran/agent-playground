"""
Configurações específicas para modelos Gemini
"""

import os
from typing import Dict, Any

def get_gemini_config() -> Dict[str, Any]:
    """
    Configurações otimizadas para Gemini visando melhor latência.
    
    AFC (Automated Function Calling) pode impactar a latência pois faz múltiplas
    chamadas remotas. Para melhorar performance:
    - Reduzir max_remote_calls 
    - Ajustar temperature para respostas mais diretas
    - Configurar timeouts apropriados
    """
    return {
        # Configurações de latência
        "temperature": float(os.getenv("GEMINI_TEMPERATURE", "0.3")),  # Respostas mais diretas
        "max_tokens": int(os.getenv("GEMINI_MAX_TOKENS", "2048")),
        "timeout": int(os.getenv("GEMINI_TIMEOUT", "30")),  # segundos
        
        # AFC (Automated Function Calling) - controla quantas chamadas remotas
        "max_remote_calls": int(os.getenv("GEMINI_MAX_REMOTE_CALLS", "3")),  # Reduzido de 10 para 3
        "enable_afc": os.getenv("GEMINI_ENABLE_AFC", "true").lower() == "true",
        
        # Performance
        "model_id": os.getenv("GEMINI_MODEL_ID", "gemini-2.0-flash-lite"),  # Mais rápido
        "streaming": os.getenv("GEMINI_STREAMING", "false").lower() == "true",
        
        # Rate limiting
        "requests_per_minute": int(os.getenv("GEMINI_RPM", "60")),
        "concurrent_requests": int(os.getenv("GEMINI_CONCURRENT", "5")),
    }

def create_optimized_gemini():
    """
    Cria uma instância do Gemini com configurações otimizadas para latência.
    """
    from agno.models.google import Gemini
    
    config = get_gemini_config()
    
    # Usar apenas parâmetros suportados pelo construtor do Gemini
    gemini_kwargs = {
        "id": config["model_id"],
        "temperature": config["temperature"],
        "max_output_tokens": config["max_tokens"],  # Usar max_output_tokens em vez de max_tokens
    }
    
    # Tentar adicionar configurações específicas se disponíveis
    # Nota: max_remote_calls pode não estar disponível no construtor
    # Será controlado por variáveis de ambiente do google-genai
    
    return Gemini(**gemini_kwargs)

def get_model_performance_tips():
    """
    Dicas para melhorar performance do modelo.
    """
    return {
        "latency_optimization": [
            "Use gemini-2.0-flash-lite para menor latência",
            "Reduza max_remote_calls para 2-3 em vez de 10",
            "Configure temperature baixa (0.1-0.3) para respostas mais diretas",
            "Use timeouts apropriados (20-30s)",
            "Limite concurrent_requests para evitar throttling"
        ],
        "afc_optimization": [
            "AFC pode fazer múltiplas chamadas sequenciais",
            "Reduza max_remote_calls se não precisar de função calling complexa",
            "Desabilite AFC completamente se não usar ferramentas",
            "Use ferramentas simples e diretas"
        ],
        "environment_variables": [
            "GEMINI_MAX_REMOTE_CALLS=3  # Reduz de 10 para 3",
            "GEMINI_TEMPERATURE=0.3     # Respostas mais diretas", 
            "GEMINI_TIMEOUT=25          # Timeout balanceado",
            "GEMINI_MODEL_ID=gemini-2.0-flash-lite  # Modelo mais rápido"
        ]
    }
