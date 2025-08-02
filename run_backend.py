#!/usr/bin/env python3
"""
🚀 Agno Teams - Backend Only

Executa apenas o backend com Teams do Agno Playground
Interface web disponível em: http://localhost:7777

Uso:
python run_backend.py
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from backend import main

if __name__ == "__main__":
    print("🚀 Iniciando Agno Teams Backend...")
    print("=" * 50)
    print("🌐 API REST: http://localhost:7777")
    print("📖 Documentação: http://localhost:7777/docs")
    print("🔍 Status: http://localhost:7777/v1/playground/status")
    print("=" * 50)
    main()
