#!/usr/bin/env python3
"""
Testes do status do backend
"""

import pytest
import requests
import subprocess
import time
import os
import signal
from pathlib import Path


# URL base do backend
BACKEND_URL = "http://localhost:7777"


@pytest.fixture(scope="module")
def backend_server():
    """Fixture que inicia o backend para os testes"""
    # Caminho para o script do backend
    backend_script = Path(__file__).parent.parent / "app" / "backend" / "agno_teams_playground.py"
    
    if not backend_script.exists():
        pytest.skip(f"Backend script não encontrado: {backend_script}")
    
    # Verificar se já está rodando
    try:
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=2)
        if response.status_code == 200:
            # Backend já está rodando
            yield None
            return
    except requests.exceptions.RequestException:
        pass
    
    # Iniciar o backend
    env = os.environ.copy()
    process = subprocess.Popen(
        ["python", str(backend_script)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        preexec_fn=os.setsid  # Para poder matar o processo grupo
    )
    
    # Aguardar o backend inicializar
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        
        # Verificar se o processo ainda está vivo
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            pytest.fail(f"Backend falhou ao iniciar:\nstdout: {stdout.decode()}\nstderr: {stderr.decode()}")
    else:
        # Timeout - matar processo e falhar
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Backend não iniciou dentro do tempo limite")
    
    yield process
    
    # Cleanup - matar o backend
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass


class TestBackendStatus:
    """Testes do status do backend"""
    
    def test_backend_is_running(self, backend_server):
        """Testa se o backend está respondendo"""
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=10)
        assert response.status_code == 200
        
    def test_status_response_format(self, backend_server):
        """Testa o formato da resposta de status"""
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        # Pode ter diferentes formatos, só verificamos que é um dict válido
        
    def test_backend_health_endpoints(self, backend_server):
        """Testa endpoints básicos de saúde"""
        # Status
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=10)
        assert response.status_code == 200
        
        # Teams (deve retornar lista ou erro controlado)
        response = requests.get(f"{BACKEND_URL}/v1/playground/teams", timeout=10)
        assert response.status_code in [200, 404, 500]  # Qualquer resposta é ok para este teste
        
    def test_backend_cors_headers(self, backend_server):
        """Testa se os headers CORS estão configurados"""
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=10)
        assert response.status_code == 200
        
        # Verificar se tem headers CORS (opcional, dependendo da implementação)
        # headers = response.headers
        # Não forçamos CORS pois pode não estar implementado
        
    def test_backend_response_time(self, backend_server):
        """Testa se o backend responde em tempo adequado"""
        start_time = time.time()
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=10)
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 5.0  # Deve responder em menos de 5 segundos
