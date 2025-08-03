#!/usr/bin/env python3
"""
Teste para verificar se o frontend corrigido funciona
"""

import requests
import sys

def test_backend_connection():
    """Testa conexão com backend"""
    try:
        response = requests.get("http://localhost:7777/v1/playground/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend conectado:", response.json())
            return True
        else:
            print("❌ Backend respondeu com erro:", response.status_code)
            return False
    except Exception as e:
        print("❌ Backend offline:", e)
        return False

def test_teams_list():
    """Testa listagem de teams"""
    try:
        response = requests.get("http://localhost:7777/v1/playground/teams", timeout=10)
        if response.status_code == 200:
            teams = response.json()
            print(f"✅ Teams disponíveis: {len(teams)}")
            if teams:
                team = teams[0]
                print(f"   - Team ID: {team.get('team_id')}")
                print(f"   - Nome: {team.get('name')}")
                return team.get('team_id')
            return None
        else:
            print("❌ Erro ao buscar teams:", response.status_code)
            return None
    except Exception as e:
        print("❌ Erro na requisição de teams:", e)
        return None

def test_send_message(team_id):
    """Testa envio de mensagem usando formato correto"""
    try:
        # Usar multipart/form-data como o frontend corrigido
        files = {
            'message': (None, 'Teste do frontend corrigido - está funcionando?'),
            'stream': (None, 'false')
        }
        
        response = requests.post(
            f"http://localhost:7777/v1/playground/teams/{team_id}/runs",
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Mensagem enviada com sucesso!")
            
            # Processar resposta
            if isinstance(result, dict):
                content = result.get("content", str(result))
                print(f"📝 Resposta: {content[:200]}...")
            elif isinstance(result, list):
                full_content = ""
                for event in result:
                    if event.get("content"):
                        full_content += event["content"]
                print(f"📝 Resposta: {full_content[:200]}...")
            
            return True
        else:
            print(f"❌ Erro ao enviar mensagem: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print("❌ Erro na requisição:", e)
        return False

def main():
    print("🧠 Teste do Frontend Streamlit Corrigido")
    print("=" * 50)
    
    # Teste 1: Backend
    if not test_backend_connection():
        print("\n❌ Backend não está rodando. Execute primeiro:")
        print("   python agno_teams_playground.py")
        sys.exit(1)
    
    # Teste 2: Teams
    team_id = test_teams_list()
    if not team_id:
        print("\n❌ Nenhum team disponível")
        sys.exit(1)
    
    # Teste 3: Mensagem
    if test_send_message(team_id):
        print("\n✅ Frontend corrigido funcionando perfeitamente!")
        print("🎉 Agora você pode usar o Streamlit normalmente")
    else:
        print("\n❌ Ainda há problemas com o envio de mensagens")
        sys.exit(1)

if __name__ == "__main__":
    main()
