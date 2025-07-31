import os
from typing import Dict, Any, Optional

def load_config() -> Dict[str, Any]:
    """Carrega configurações do ambiente e valores padrão."""
    return {
        # API Keys
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        
        # Servidor
        "host": os.getenv("HOST", "localhost"),
        "port": int(os.getenv("PORT", 7777)),
        
        # Storage
        "storage_dir": os.getenv("STORAGE_DIR", "storage"),
        "db_file": os.getenv("DB_FILE", "agents.db"),
        
        # MCP
        "mcp_enabled": os.getenv("MCP_ENABLED", "true").lower() == "true",
        "mcp_server_port": int(os.getenv("MCP_SERVER_PORT", 8888)),
        
        # Logging
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_file": os.getenv("LOG_FILE", "logs/agno_playground.log"),
    }

def get_storage_path(filename: str) -> str:
    """Retorna o caminho completo para um arquivo de storage."""
    config = load_config()
    storage_dir = config["storage_dir"]
    os.makedirs(storage_dir, exist_ok=True)
    return os.path.join(storage_dir, filename)

def validate_config(test_mode: bool = False) -> bool:
    """Valida se as configurações obrigatórias estão presentes."""
    config = load_config()
    
    if not config["google_api_key"]:
        print("❌ GOOGLE_API_KEY não encontrada. Configure no arquivo .env")
        return False
    
    # No modo de teste, aceita chaves dummy
    if test_mode and config["google_api_key"] in ["test_key_for_development", "your_google_api_key_here"]:
        print("⚠️  Modo de teste: usando chave dummy para desenvolvimento")
        return True
    
    # Verifica se não é uma chave placeholder
    if config["google_api_key"] in ["test_key_for_development", "your_google_api_key_here"]:
        print("❌ GOOGLE_API_KEY é uma chave de exemplo. Configure uma chave real no arquivo .env")
        print("💡 Para obter uma chave: https://makersuite.google.com/app/apikey")
        return False
    
    print("✅ Configurações validadas com sucesso!")
    return True
