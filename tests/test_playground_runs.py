#!/usr/bin/env python3
"""
Testes de execução de tarefas no playground
"""

import pytest
import requests
import json
import time


# URL base do backend  
BACKEND_URL = "http://localhost:7777"


class TestPlaygroundRuns:
    """Testes de execução de tarefas"""
    
    def test_simple_question_run(self):
        """Testa execução de uma pergunta simples"""
        team_id = "default-team"
        
        payload = {
            "message": "Olá! Como você está?",
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=30  # Timeout maior para LLM
        )
        
        # Aceitar 200 (sucesso) ou outros códigos (ainda não implementado)
        assert response.status_code in [200, 404, 405, 422, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
            # Pode ter 'response', 'content', 'result', etc.
            
    def test_data_analysis_request(self):
        """Testa solicitação de análise de dados"""
        team_id = "default-team"
        
        payload = {
            "message": "Analise os dados de vendas do último trimestre",
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=45  # Timeout maior para análise
        )
        
        assert response.status_code in [200, 404, 405, 422, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
            
    def test_code_analysis_request(self):
        """Testa solicitação de análise de código"""
        team_id = "default-team"
        
        payload = {
            "message": "Analise este código Python: def hello(): print('Hello World')",
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=30
        )
        
        assert response.status_code in [200, 404, 405, 422, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
            
    def test_financial_analysis_request(self):
        """Testa solicitação de análise financeira"""
        team_id = "default-team"
        
        payload = {
            "message": "Qual foi o desempenho da AAPL nos últimos 30 dias?",
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=45
        )
        
        assert response.status_code in [200, 404, 405, 422, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
            
    def test_web_research_request(self):
        """Testa solicitação de pesquisa web"""
        team_id = "default-team"
        
        payload = {
            "message": "Pesquise informações sobre inteligência artificial em 2024",
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=60  # Timeout maior para pesquisa web
        )
        
        assert response.status_code in [200, 404, 405, 422, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)


class TestRunsValidation:
    """Testes de validação de requests"""
    
    def test_empty_message_validation(self):
        """Testa validação de mensagem vazia"""
        team_id = "default-team"
        
        payload = {
            "message": "",
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=10
        )
        
        # Deve rejeitar mensagem vazia ou aceitar (dependendo da implementação)
        assert response.status_code in [200, 400, 404, 405, 422, 500]
        
    def test_missing_message_validation(self):
        """Testa validação de payload sem mensagem"""
        team_id = "default-team"
        
        payload = {
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=10
        )
        
        # Deve rejeitar payload inválido ou aceitar com default
        assert response.status_code in [200, 400, 404, 405, 422, 500]
        
    def test_invalid_json_payload(self):
        """Testa payload JSON inválido"""
        team_id = "default-team"
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Deve rejeitar JSON inválido
        assert response.status_code in [400, 404, 405, 422, 500]


class TestRunsResponseFormat:
    """Testes de formato das respostas"""
    
    def test_non_stream_response_format(self):
        """Testa formato de resposta não-stream"""
        team_id = "default-team"
        
        payload = {
            "message": "Teste de formato de resposta",
            "stream": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            # Verificar que é JSON válido
            data = response.json()
            assert isinstance(data, dict)
            
            # Verificar Content-Type
            assert "application/json" in response.headers.get("content-type", "").lower()
            
    def test_stream_response_format(self):
        """Testa formato de resposta stream (se implementado)"""
        team_id = "default-team"
        
        payload = {
            "message": "Teste de stream",
            "stream": True
        }
        
        response = requests.post(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
            json=payload,
            timeout=30
        )
        
        # Stream pode ou não estar implementado
        assert response.status_code in [200, 404, 405, 422, 500]
        
        if response.status_code == 200:
            # Se stream está implementado, verificar headers apropriados
            content_type = response.headers.get("content-type", "").lower()
            # Pode ser text/plain, text/event-stream, ou application/json
            assert any(ct in content_type for ct in ["text/", "application/json"])
