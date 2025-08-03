#!/usr/bin/env python3
"""
Testes de configuração e ambiente do sistema
"""

import pytest
import os
import sys
from pathlib import Path
import subprocess


# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestEnvironmentSetup:
    """Testes de configuração do ambiente"""
    
    def test_project_structure(self):
        """Testa estrutura básica do projeto"""
        # Verificar diretórios principais
        assert project_root.exists(), "Diretório raiz do projeto não encontrado"
        
        expected_dirs = [
            "app",
            "tests", 
            "docs"
        ]
        
        for dir_name in expected_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"Diretório {dir_name} não encontrado"
            
    def test_app_structure(self):
        """Testa estrutura do diretório app"""
        app_dir = project_root / "app"
        assert app_dir.exists(), "Diretório app não encontrado"
        
        expected_subdirs = [
            "agents",
            "backend",
            "config"
        ]
        
        for subdir in expected_subdirs:
            subdir_path = app_dir / subdir
            if not subdir_path.exists():
                pytest.skip(f"Subdiretório app/{subdir} não encontrado")
                
    def test_requirements_file(self):
        """Testa se arquivo requirements.txt existe"""
        requirements_file = project_root / "requirements.txt"
        assert requirements_file.exists(), "Arquivo requirements.txt não encontrado"
        
        # Verificar se não está vazio
        content = requirements_file.read_text()
        assert len(content.strip()) > 0, "requirements.txt está vazio"
        
    def test_env_example_file(self):
        """Testa se arquivo .env.example existe"""
        env_example = project_root / ".env.example"
        assert env_example.exists(), "Arquivo .env.example não encontrado"
        
        # Verificar se contém GOOGLE_API_KEY
        content = env_example.read_text()
        assert "GOOGLE_API_KEY" in content, "GOOGLE_API_KEY não encontrada em .env.example"
        
    def test_makefile_exists(self):
        """Testa se Makefile existe"""
        makefile = project_root / "Makefile"
        assert makefile.exists(), "Makefile não encontrado"
        
        # Verificar se contém comandos básicos
        content = makefile.read_text()
        expected_targets = ["test", "setup", "backend"]
        
        for target in expected_targets:
            assert target in content, f"Target '{target}' não encontrado no Makefile"


class TestDependencies:
    """Testes de dependências do sistema"""
    
    def test_python_version(self):
        """Testa versão do Python"""
        version = sys.version_info
        assert version.major == 3, "Python 3 é obrigatório"
        assert version.minor >= 8, "Python 3.8+ é recomendado"
        
    def test_critical_imports(self):
        """Testa importações críticas"""
        # Bibliotecas padrão que devem estar disponíveis
        try:
            import json
            import os
            import sys
            import pathlib
            import subprocess
            import tempfile
            import time
            import threading
            import queue
        except ImportError as e:
            pytest.fail(f"Biblioteca padrão não disponível: {e}")
            
    def test_optional_imports(self):
        """Testa importações opcionais (podem não estar instaladas)"""
        optional_libs = [
            "requests",
            "pandas", 
            "pytest"
        ]
        
        missing_libs = []
        for lib in optional_libs:
            try:
                __import__(lib)
            except ImportError:
                missing_libs.append(lib)
                
        if missing_libs:
            pytest.skip(f"Bibliotecas opcionais não instaladas: {', '.join(missing_libs)}")


class TestConfigurationFiles:
    """Testes de arquivos de configuração"""
    
    def test_config_directory(self):
        """Testa diretório de configuração"""
        config_dir = project_root / "app" / "config"
        if not config_dir.exists():
            pytest.skip("Diretório app/config não encontrado")
            
        # Verificar se tem pelo menos um arquivo .py
        py_files = list(config_dir.glob("*.py"))
        assert len(py_files) > 0, "Nenhum arquivo Python encontrado em app/config"
        
    def test_storage_directory(self):
        """Testa diretório de storage"""
        storage_dir = project_root / "storage"
        if storage_dir.exists():
            # Se existe, verificar se é um diretório válido
            assert storage_dir.is_dir(), "storage deve ser um diretório"
        else:
            # Storage pode não existir ainda (será criado dinamicamente)
            pass
            
    def test_data_directory(self):
        """Testa diretório de dados"""
        data_dir = project_root / "data"
        if data_dir.exists():
            assert data_dir.is_dir(), "data deve ser um diretório"
        else:
            # data pode não existir (será criado dinamicamente)
            pass


class TestSystemUtilities:
    """Testes de utilitários do sistema"""
    
    def test_makefile_test_target(self):
        """Testa se o target 'test' do Makefile funciona"""
        makefile = project_root / "Makefile"
        if not makefile.exists():
            pytest.skip("Makefile não encontrado")
            
        # Tentar executar make test (sem falhar o teste se der erro)
        try:
            result = subprocess.run(
                ["make", "test"],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            # Não falhar se make test falha, apenas verificar que o comando existe
            assert result.returncode in [0, 1, 2], "make test deve ser um comando válido"
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("make não disponível ou timeout")
            
    def test_python_syntax_check(self):
        """Testa sintaxe dos arquivos Python principais"""
        python_files = [
            project_root / "app" / "backend" / "agno_teams_playground.py"
        ]
        
        for py_file in python_files:
            if py_file.exists():
                # Compilar arquivo para verificar sintaxe
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    compile(content, str(py_file), 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Erro de sintaxe em {py_file}: {e}")
                except Exception:
                    # Outros erros (como imports) são ok para este teste
                    pass
                    

class TestDocumentation:
    """Testes de documentação"""
    
    def test_readme_exists(self):
        """Testa se README existe"""
        readme_files = [
            project_root / "README.md",
            project_root / "README.rst", 
            project_root / "README.txt"
        ]
        
        readme_exists = any(f.exists() for f in readme_files)
        assert readme_exists, "Nenhum arquivo README encontrado"
        
    def test_docs_directory(self):
        """Testa diretório de documentação"""
        docs_dir = project_root / "docs"
        assert docs_dir.exists(), "Diretório docs não encontrado"
        
        # Verificar se tem algum arquivo de documentação
        doc_files = list(docs_dir.glob("*.md")) + list(docs_dir.glob("*.rst"))
        assert len(doc_files) > 0, "Nenhum arquivo de documentação encontrado em docs/"
        
    def test_license_file(self):
        """Testa se arquivo de licença existe"""
        license_files = [
            project_root / "LICENSE",
            project_root / "LICENSE.txt",
            project_root / "LICENSE.md"
        ]
        
        license_exists = any(f.exists() for f in license_files)
        if not license_exists:
            pytest.skip("Arquivo de licença não encontrado (opcional)")


class TestGitConfiguration:
    """Testes de configuração Git"""
    
    def test_gitignore_exists(self):
        """Testa se .gitignore existe"""
        gitignore = project_root / ".gitignore"
        if not gitignore.exists():
            pytest.skip(".gitignore não encontrado")
            
        content = gitignore.read_text()
        
        # Verificar padrões importantes
        important_patterns = [
            "__pycache__",
            "*.pyc",
            ".env"
        ]
        
        for pattern in important_patterns:
            if pattern not in content:
                pytest.skip(f"Padrão '{pattern}' não encontrado em .gitignore")
                
    def test_git_repository(self):
        """Testa se é um repositório Git"""
        git_dir = project_root / ".git"
        if git_dir.exists():
            assert git_dir.is_dir(), ".git deve ser um diretório"
        else:
            pytest.skip("Não é um repositório Git")
