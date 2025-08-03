#!/usr/bin/env python3
"""
🚀 Agno Teams - Backend Simplificado para Teste

Versão básica para verificar se conseguimos resolver o problema do make full
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

try:
    from agno.playground import Playground
    from agents.teams_manager import teams_manager
    print("✅ Imports básicos OK")
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    sys.exit(1)

def main():
    """Função principal simplificada."""
    
    print("🔍 Verificando configuração...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY não encontrada!")
        print("Configure no arquivo .env:")
        print("GOOGLE_API_KEY=sua_api_key_aqui")
        return
        
    print("✅ API Key configurada!")
    print("🎮 Inicializando teams...")
    
    try:
        # Inicializar teams usando o manager existente
        teams = teams_manager.initialize_all_teams()
        
        if not teams:
            print("❌ Nenhum team foi criado")
            return
            
        # Pegar o team principal
        main_team = teams.get("main")
        if not main_team:
            print("❌ Team principal não encontrado")
            return
            
        print(f"✅ Team principal criado: {main_team.name}")
        
        # Criar playground com teams
        playground = Playground(
            teams=[main_team],
            name="Agno Teams Backend Simplificado"
        )
        
        print("🌐 Playground criado!")
        print("🚀 Iniciando servidor na porta 7777...")
        
        # Servir playground
        app = playground.get_app()
        playground.serve(app, port=7777, host="0.0.0.0")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
