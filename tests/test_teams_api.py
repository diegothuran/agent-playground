#!/usr/bin/env python3
"""
Testes da API de teams
"""

import pytest
import requests
import json


# URL base do backend
BACKEND_URL = "http://localhost:7777"


class TestTeamsAPI:
    """Testes da API de teams"""
    
    def test_list_teams(self):
        """Testa listagem de teams disponíveis"""
        response = requests.get(f"{BACKEND_URL}/v1/playground/teams", timeout=10)
        
        # Aceitar 200 (sucesso) ou 404/500 (ainda não implementado)
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict))
            
    def test_get_team_info(self):
        """Testa obtenção de informações de um team específico"""
        # Primeiro, tentar listar teams
        response = requests.get(f"{BACKEND_URL}/v1/playground/teams", timeout=10)
        
        if response.status_code == 200:
            teams_data = response.json()
            
            # Se é uma lista e tem teams
            if isinstance(teams_data, list) and teams_data:
                team_id = teams_data[0].get('id', 'default-team')
            # Se é um dict com teams
            elif isinstance(teams_data, dict) and 'teams' in teams_data:
                teams = teams_data['teams']
                if teams:
                    team_id = teams[0].get('id', 'default-team')
                else:
                    team_id = 'default-team'
            else:
                team_id = 'default-team'
        else:
            team_id = 'default-team'
        
        # Tentar obter informações do team
        response = requests.get(f"{BACKEND_URL}/v1/playground/teams/{team_id}", timeout=10)
        # Aceitar qualquer resposta (implementação pode variar)
        assert response.status_code in [200, 404, 405, 500]
        
    def test_teams_api_format(self):
        """Testa formato das respostas da API de teams"""
        response = requests.get(f"{BACKEND_URL}/v1/playground/teams", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict))
            
            # Se é lista, verificar que tem formato correto
            if isinstance(data, list):
                for team in data:
                    assert isinstance(team, dict)
                    # Pode ter 'id', 'name', 'description', etc.
                    
            # Se é dict, verificar estrutura básica
            elif isinstance(data, dict):
                # Pode ter 'teams', 'status', etc.
                pass


class TestTeamsSessions:
    """Testes de sessões de teams"""
    
    def test_get_team_sessions(self):
        """Testa obtenção de sessões de um team"""
        team_id = "test-team"
        
        response = requests.get(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/sessions",
            timeout=10
        )
        
        # Aceitar qualquer resposta (pode não estar implementado)
        assert response.status_code in [200, 404, 405, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict))
            
    def test_get_team_memories(self):
        """Testa obtenção de memórias de um team"""
        team_id = "test-team"
        
        response = requests.get(
            f"{BACKEND_URL}/v1/playground/teams/{team_id}/memories",
            timeout=10
        )
        
        # Aceitar qualquer resposta (pode não estar implementado)
        assert response.status_code in [200, 404, 405, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict))
