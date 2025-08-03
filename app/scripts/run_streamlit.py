#!/usr/bin/env python3
"""
🚀 Agno Teams - Frontend Streamlit

Executa o frontend Streamlit para o Agno Teams Playground.

Uso:
python run_streamlit.py
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Iniciando Agno Teams Frontend (Streamlit)...")
    print("=" * 50)
    print("🌐 Interface: http://localhost:8501")
    print("📖 Certifique-se que o backend está rodando na porta 7777")
    print("=" * 50)
    
    # Adicionar o diretório raiz ao path
    sys.path.append(str(Path(__file__).parent))
    
    # Executar streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Frontend encerrado pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
