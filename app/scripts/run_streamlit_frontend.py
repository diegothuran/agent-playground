#!/usr/bin/env python3
"""
🧠 Agno Teams - Executar Frontend Streamlit

Script para iniciar o frontend Streamlit que consome o playground backend.

Uso:
python run_streamlit_frontend.py
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🧠 Agno Teams - Frontend Streamlit")
    print("=" * 50)
    print("🌐 Interface será aberta em: http://localhost:8501")
    print("⚠️  Certifique-se que o backend está rodando em: http://localhost:7777")
    print("   Execute: python app/backend/agno_teams_playground.py")
    print("=" * 50)
    
    # Verificar se streamlit está instalado
    try:
        import streamlit
    except ImportError:
        print("📦 Streamlit não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "plotly"], check=True)
    
    # Executar streamlit
    try:
        # Obter caminho da raiz do projeto
        project_root = Path(__file__).parent.parent.parent
        frontend_script = project_root / "app" / "frontend" / "streamlit_frontend.py"
        
        streamlit_cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(frontend_script),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "light"
        ]
        
        print("🚀 Iniciando Streamlit...")
        # Mudar para o diretório raiz do projeto
        os.chdir(str(project_root))
        subprocess.run(streamlit_cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Frontend encerrado pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Streamlit: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
