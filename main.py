#!/usr/bin/env python3
"""
🧠 Agno Teams - Sistema de Agentes Especializados

Sistema moderno de agentes especializados usando o framework Agno,
com arquitetura de Teams inteligente que analisa contexto e orquestra 
especialistas automaticamente.

Uso:
    python main.py --mode [backend|frontend|full]
    
Ou use os comandos make:
    make backend    # Apenas backend API (porta 7777)
    make frontend   # Apenas frontend Streamlit (porta 8501)  
    make full       # Sistema completo
"""

import argparse
import sys
import subprocess
from pathlib import Path

def run_backend():
    """Executa apenas o backend"""
    print("🔗 Iniciando Agno Teams Backend...")
    subprocess.run([sys.executable, "app/backend/agno_teams_playground.py"])

def run_frontend():
    """Executa apenas o frontend"""
    print("🎨 Iniciando Agno Teams Frontend...")
    subprocess.run([sys.executable, "app/scripts/run_streamlit_frontend.py"])

def run_full():
    """Executa o sistema completo"""
    print("🚀 Iniciando Sistema Completo Agno Teams...")
    subprocess.run([sys.executable, "app/scripts/run_full_streamlit.py"])

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="🧠 Agno Teams - Sistema de Agentes Especializados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --mode backend    # Apenas backend
  python main.py --mode frontend   # Apenas frontend  
  python main.py --mode full       # Sistema completo
  
Ou use make:
  make backend
  make frontend
  make full
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["backend", "frontend", "full"],
        default="full",
        help="Modo de execução (padrão: full)"
    )
    
    args = parser.parse_args()
    
    print(f"🧠 Agno Teams - Modo: {args.mode}")
    print("=" * 50)
    
    if args.mode == "backend":
        run_backend()
    elif args.mode == "frontend":
        run_frontend()
    elif args.mode == "full":
        run_full()

if __name__ == "__main__":
    main()
