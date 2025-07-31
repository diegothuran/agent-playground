"""
Testes básicos para o playground Agno.
Execute com: python -m pytest tests/ -v
"""

import pytest
import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import load_config, validate_config, get_storage_path
from utils import validate_api_key, check_dependencies, format_timestamp

class TestConfig:
    """Testes para as configurações."""
    
    def test_load_config(self):
        """Testa se as configurações são carregadas corretamente."""
        config = load_config()
        
        assert isinstance(config, dict)
        assert "host" in config
        assert "port" in config
        assert "storage_dir" in config
    
    def test_get_storage_path(self):
        """Testa a geração de caminhos de storage."""
        path = get_storage_path("test.db")
        
        assert isinstance(path, str)
        assert path.endswith("test.db")
        assert "storage" in path

class TestUtils:
    """Testes para utilitários."""
    
    def test_validate_api_key_valid(self):
        """Testa validação de chave API válida."""
        valid_key = "sk-1234567890abcdef"
        assert validate_api_key(valid_key) == True
    
    def test_validate_api_key_invalid(self):
        """Testa validação de chave API inválida."""
        invalid_keys = [
            "",
            "short",
            "your_api_key_here",
            None
        ]
        
        for key in invalid_keys:
            assert validate_api_key(key) == False
    
    def test_format_timestamp(self):
        """Testa formatação de timestamp."""
        from datetime import datetime
        
        timestamp = datetime(2023, 12, 25, 15, 30, 45)
        formatted = format_timestamp(timestamp)
        
        assert formatted == "2023-12-25 15:30:45"
    
    def test_check_dependencies(self):
        """Testa verificação de dependências."""
        deps = check_dependencies()
        
        assert isinstance(deps, dict)
        assert "requests" in deps  # requests deve estar disponível

class TestTools:
    """Testes para ferramentas customizadas."""
    
    def test_code_analysis_tools_import(self):
        """Testa se as ferramentas de análise de código podem ser importadas."""
        try:
            from tools.code_tools import CodeAnalysisTools
            tools = CodeAnalysisTools()
            assert tools is not None
        except ImportError:
            pytest.skip("Agno não está instalado")
    
    def test_data_analysis_tools_import(self):
        """Testa se as ferramentas de análise de dados podem ser importadas."""
        try:
            from tools.data_tools import DataAnalysisTools
            tools = DataAnalysisTools()
            assert tools is not None
        except ImportError:
            pytest.skip("Dependências de análise de dados não estão instaladas")

class TestMCP:
    """Testes para funcionalidades MCP."""
    
    def test_mcp_tools_import(self):
        """Testa se as ferramentas MCP podem ser importadas."""
        try:
            from mcp.mcp_tools import MCPTools
            tools = MCPTools()
            assert tools is not None
        except ImportError:
            pytest.skip("Agno não está instalado")
    
    def test_mcp_config_exists(self):
        """Testa se o arquivo de configuração MCP existe."""
        config_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "mcp", 
            "config.json"
        )
        assert os.path.exists(config_path)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
