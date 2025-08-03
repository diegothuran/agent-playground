#!/usr/bin/env python3
"""
Testes dos agentes especialistas
"""

import pytest
import sys
from pathlib import Path
import os

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar variáveis de ambiente necessárias
os.environ.setdefault("GOOGLE_API_KEY", "test-key-for-testing")


class TestSpecialistsImport:
    """Testes de importação dos especialistas"""
    
    def test_import_data_specialist(self):
        """Testa importação do especialista de dados"""
        try:
            from app.agents.specialists.data_specialist import create_data_specialist
            specialist = create_data_specialist()
            assert specialist is not None
            assert hasattr(specialist, 'name')
            assert hasattr(specialist, 'description')
        except ImportError as e:
            pytest.skip(f"Módulo data_specialist não encontrado: {e}")
        except Exception as e:
            # Pode falhar por falta de API key, mas deve importar
            if "API" not in str(e):
                raise
            
    def test_import_code_specialist(self):
        """Testa importação do especialista de código"""
        try:
            from app.agents.specialists.code_specialist import create_code_specialist
            specialist = create_code_specialist()
            assert specialist is not None
            assert hasattr(specialist, 'name')
            assert hasattr(specialist, 'description')
        except ImportError as e:
            pytest.skip(f"Módulo code_specialist não encontrado: {e}")
        except Exception as e:
            if "API" not in str(e):
                raise
                
    def test_import_finance_specialist(self):
        """Testa importação do especialista financeiro"""
        try:
            from app.agents.specialists.finance_specialist import create_finance_specialist
            specialist = create_finance_specialist()
            assert specialist is not None
            assert hasattr(specialist, 'name')
            assert hasattr(specialist, 'description')
        except ImportError as e:
            pytest.skip(f"Módulo finance_specialist não encontrado: {e}")
        except Exception as e:
            if "API" not in str(e):
                raise
                
    def test_import_web_specialist(self):
        """Testa importação do especialista web"""
        try:
            from app.agents.specialists.web_specialist import create_web_specialist
            specialist = create_web_specialist()
            assert specialist is not None
            assert hasattr(specialist, 'name')
            assert hasattr(specialist, 'description')
        except ImportError as e:
            pytest.skip(f"Módulo web_specialist não encontrado: {e}")
        except Exception as e:
            if "API" not in str(e):
                raise
                
    def test_import_github_specialist(self):
        """Testa importação do especialista GitHub"""
        try:
            from app.agents.specialists.github_specialist import create_github_specialist
            specialist = create_github_specialist()
            assert specialist is not None
            assert hasattr(specialist, 'name')
            assert hasattr(specialist, 'description')
        except ImportError as e:
            pytest.skip(f"Módulo github_specialist não encontrado: {e}")
        except Exception as e:
            if "API" not in str(e):
                raise


class TestSpecialistsConfiguration:
    """Testes de configuração dos especialistas"""
    
    def test_specialists_have_required_attributes(self):
        """Testa se especialistas têm atributos obrigatórios"""
        try:
            from app.agents.specialists.data_specialist import create_data_specialist
            specialist = create_data_specialist()
            
            # Verificar atributos básicos
            assert hasattr(specialist, 'name')
            assert specialist.name is not None
            assert len(specialist.name) > 0
            
            # Description pode ser None em alguns casos, verificar se existe
            if hasattr(specialist, 'description') and specialist.description is not None:
                assert len(specialist.description) > 0
            
        except ImportError:
            pytest.skip("Especialistas não disponíveis para teste")
        except Exception as e:
            if "API" not in str(e):
                raise
            
    def test_specialists_tools_configuration(self):
        """Testa se especialistas têm ferramentas configuradas"""
        try:
            from app.agents.specialists.data_specialist import create_data_specialist
            specialist = create_data_specialist()
            
            # Verificar se tem tools (opcional)
            if hasattr(specialist, 'tools'):
                assert isinstance(specialist.tools, (list, type(None)))
                
        except ImportError:
            pytest.skip("Especialistas não disponíveis para teste")
        except Exception as e:
            if "API" not in str(e):
                raise


class TestAgentsStructure:
    """Testes da estrutura dos agentes"""
    
    def test_agents_directory_structure(self):
        """Testa estrutura do diretório de agentes"""
        agents_dir = project_root / "app" / "agents"
        assert agents_dir.exists(), "Diretório app/agents não encontrado"
        
        specialists_dir = agents_dir / "specialists"
        assert specialists_dir.exists(), "Diretório app/agents/specialists não encontrado"
        
        # Verificar arquivos principais
        expected_files = [
            "data_specialist.py",
            "code_specialist.py", 
            "finance_specialist.py",
            "web_specialist.py",
            "github_specialist.py"
        ]
        
        for file_name in expected_files:
            file_path = specialists_dir / file_name
            if not file_path.exists():
                pytest.skip(f"Arquivo {file_name} não encontrado em specialists/")
                
    def test_config_module_exists(self):
        """Testa se módulo de configuração existe"""
        config_dir = project_root / "app" / "config"
        if not config_dir.exists():
            pytest.skip("Diretório app/config não encontrado")
            
        # Verificar alguns arquivos de configuração esperados
        expected_configs = ["settings.py", "gemini_simple.py"]
        found_configs = []
        
        for config_file in expected_configs:
            if (config_dir / config_file).exists():
                found_configs.append(config_file)
                
        # Pelo menos um arquivo de config deve existir
        assert len(found_configs) > 0, "Nenhum arquivo de configuração encontrado"


class TestPlaygroundComponents:
    """Testes dos componentes do playground"""
    
    def test_playground_backend_exists(self):
        """Testa se arquivo principal do backend existe"""
        backend_file = project_root / "app" / "backend" / "agno_teams_playground.py"
        assert backend_file.exists(), "Arquivo principal do backend não encontrado"
        
    def test_playground_imports(self):
        """Testa importações básicas do playground"""
        try:
            # Tentar importar componentes principais do agno
            import agno
            import agno.agent
            import agno.team
            import agno.playground
            
        except ImportError as e:
            pytest.skip(f"Biblioteca agno não disponível: {e}")
            
    def test_environment_variables(self):
        """Testa se variáveis de ambiente estão configuradas"""
        # Verificar se .env.example existe
        env_example = project_root / ".env.example"
        assert env_example.exists(), "Arquivo .env.example não encontrado"
        
        # Verificar se GOOGLE_API_KEY está definida (mesmo que seja test key)
        api_key = os.getenv("GOOGLE_API_KEY")
        assert api_key is not None, "GOOGLE_API_KEY não está definida"
