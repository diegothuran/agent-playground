"""
Utilitários e funções auxiliares para o playground Agno.
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Configura o sistema de logging."""
    
    # Cria diretório de logs se necessário
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    # Configuração do logging
    logging_config = {
        'level': getattr(logging, log_level.upper()),
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }
    
    if log_file:
        logging_config['filename'] = log_file
    
    logging.basicConfig(**logging_config)
    
    # Log inicial
    logger = logging.getLogger(__name__)
    logger.info(f"Sistema de logging configurado - Nível: {log_level}")
    
    return logger

def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Formata um timestamp para exibição."""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def validate_api_key(api_key: str, service_name: str = "API") -> bool:
    """Valida se uma chave de API está presente e tem formato básico."""
    if not api_key:
        return False
    
    # Validações básicas
    if len(api_key) < 10:
        return False
    
    if api_key.startswith("your_") or api_key.endswith("_here"):
        return False
    
    return True

def create_agent_summary(agent) -> dict:
    """Cria um resumo das informações de um agente."""
    return {
        "name": getattr(agent, 'name', 'Unknown'),
        "model": str(getattr(agent, 'model', 'Unknown')),
        "tools_count": len(getattr(agent, 'tools', [])),
        "has_storage": hasattr(agent, 'storage') and agent.storage is not None,
        "markdown_enabled": getattr(agent, 'markdown', False),
        "history_enabled": getattr(agent, 'add_history_to_messages', False)
    }

def check_dependencies() -> dict:
    """Verifica se as dependências estão instaladas."""
    dependencies = {
        'agno': False,
        'openai': False,
        'pandas': False,
        'numpy': False,
        'matplotlib': False,
        'requests': False
    }
    
    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False
    
    return dependencies

def get_system_info() -> dict:
    """Retorna informações sobre o sistema."""
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0],
        "hostname": platform.node()
    }
