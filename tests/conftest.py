#!/usr/bin/env python3
"""
Configuração de fixtures para pytest
"""

import pytest
import pandas as pd
import tempfile
import os


@pytest.fixture
def team_id():
    """Fixture que retorna um ID de team para testes"""
    return "test-team-id-12345"


@pytest.fixture
def file_path():
    """Fixture que cria um arquivo CSV temporário para testes"""
    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("nome,idade,salario,departamento\n")
        f.write("João Silva,28,5500.50,TI\n")
        f.write("Maria Santos,35,7200.00,Financeiro\n")
        f.write("Pedro Lima,42,8900.75,Vendas\n")
        f.write("Ana Costa,31,6100.25,RH\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def df():
    """Fixture que retorna um DataFrame de exemplo"""
    try:
        import pandas as pd
        data = {
            'nome': ['João Silva', 'Maria Santos', 'Pedro Lima', 'Ana Costa'],
            'idade': [28, 35, 42, 31],
            'salario': [5500.50, 7200.00, 8900.75, 6100.25],
            'departamento': ['TI', 'Financeiro', 'Vendas', 'RH']
        }
        return pd.DataFrame(data)
    except Exception as e:
        # Se pandas não funcionar, retornar dados como dict
        return {
            'nome': ['João Silva', 'Maria Santos', 'Pedro Lima', 'Ana Costa'],
            'idade': [28, 35, 42, 31],
            'salario': [5500.50, 7200.00, 8900.75, 6100.25],
            'departamento': ['TI', 'Financeiro', 'Vendas', 'RH']
        }


@pytest.fixture
def sample_csv_content():
    """Fixture que retorna conteúdo CSV de exemplo"""
    return """nome,idade,salario,departamento
João Silva,28,5500.50,TI
Maria Santos,35,7200.00,Financeiro
Pedro Lima,42,8900.75,Vendas
Ana Costa,31,6100.25,RH
Carlos Souza,29,5800.00,TI
Lucia Oliveira,38,7500.50,Marketing"""


@pytest.fixture(scope="session")
def data_dir():
    """Fixture que retorna o diretório de dados de teste"""
    return os.path.join(os.path.dirname(__file__), '..', 'data')


@pytest.fixture(scope="session")
def backend_url():
    """Fixture que retorna a URL base do backend"""
    return "http://localhost:7777"


@pytest.fixture
def test_team_id():
    """Fixture que retorna um ID de team válido para testes"""
    return "default-team"


@pytest.fixture
def sample_payload():
    """Fixture que retorna um payload de teste padrão"""
    return {
        "message": "Teste automatizado do sistema",
        "stream": False
    }


@pytest.fixture
def project_root():
    """Fixture que retorna o caminho raiz do projeto"""
    return os.path.dirname(os.path.dirname(__file__))
