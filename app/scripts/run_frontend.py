#!/usr/bin/env python3
"""
🎨 Agno Teams - Frontend Only

Executa apenas o frontend Next.js com agno-ui
Interface web disponível em: http://localhost:3000

Uso:
python run_frontend.py

Pré-requisitos:
- Backend deve estar rodando em http://localhost:7777
- Node.js e pnpm instalados
"""

import subprocess
import sys
import os
from pathlib import Path

def check_backend():
    """Verifica se o backend está rodando."""
    try:
        import requests
        response = requests.get("http://localhost:7777/v1/playground/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("playground") == "available":
                return True
    except:
        pass
    return False

def main():
    print("🎨 Iniciando Agno Teams Frontend...")
    print("=" * 50)
    
    # Verificar se o backend está rodando
    if not check_backend():
        print("❌ Backend não detectado!")
        print("🔧 Inicie o backend primeiro: python run_backend.py")
        print("⏱️  Ou execute o sistema completo: python run_full.py")
        return
    
    print("✅ Backend detectado em http://localhost:7777")
    
    # Navegar para o diretório frontend
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print(f"❌ Diretório frontend não encontrado: {frontend_dir}")
        return
    
    os.chdir(frontend_dir)
    
    print("📦 Instalando dependências...")
    try:
        subprocess.run(["pnpm", "install"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        print("💡 Certifique-se que o pnpm está instalado: npm install -g pnpm")
        return
    except FileNotFoundError:
        print("❌ pnpm não encontrado")
        print("💡 Instale o pnpm: npm install -g pnpm")
        return
    
    print("🚀 Iniciando servidor de desenvolvimento...")
    print("🌐 Frontend: http://localhost:3000")
    print("🔗 Backend API: http://localhost:7777")
    print("=" * 50)
    
    try:
        subprocess.run(["pnpm", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Frontend encerrado pelo usuário")
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar o frontend")

if __name__ == "__main__":
    main()
