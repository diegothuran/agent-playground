#!/usr/bin/env python3
"""
🚀 Agno Teams - Sistema Completo Simplificado

Executa backend + frontend simultaneamente
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def main():
    print("🚀 Agno Teams - Sistema Completo")
    print("=" * 50)
    
    backend_process = None
    frontend_process = None
    
    try:
        # 1. Iniciar backend
        print("🚀 Iniciando backend...")
        backend_process = subprocess.Popen(
            [sys.executable, "run_backend.py"],
            cwd=Path(__file__).parent
        )
        print(f"✅ Backend iniciado (PID: {backend_process.pid})")
        
        # 2. Aguardar backend ficar pronto (verificação simples)
        print("⏱️  Aguardando backend...")
        time.sleep(5)  # Aguarda 5 segundos fixos
        
        # 3. Verificar se backend ainda está rodando
        if backend_process.poll() is not None:
            print("❌ Backend falhou ao iniciar")
            return
            
        # 4. Iniciar frontend 
        print("🎨 Iniciando frontend...")
        frontend_dir = Path(__file__).parent / "frontend"
        
        if not frontend_dir.exists():
            print(f"❌ Diretório frontend não encontrado: {frontend_dir}")
            return
        
        # Instalar dependências se necessário
        print("📦 Instalando dependências do frontend...")
        subprocess.run(["pnpm", "install"], cwd=frontend_dir, check=True)
        
        # Iniciar frontend
        frontend_process = subprocess.Popen(
            ["pnpm", "dev"],
            cwd=frontend_dir
        )
        print(f"✅ Frontend iniciado (PID: {frontend_process.pid})")
        
        # 5. Mostrar informações
        print("\n🎉 Sistema completo iniciado!")
        print("=" * 50)
        print("🌐 Frontend: http://localhost:3000")
        print("🔗 Backend API: http://localhost:7777")
        print("📖 Documentação: http://localhost:7777/docs")
        print("=" * 50)
        print("⌨️  Pressione Ctrl+C para parar")
        
        # 6. Manter rodando
        while True:
            time.sleep(1)
            
            # Verificar se processos ainda estão rodando
            if backend_process.poll() is not None:
                print("❌ Backend parou inesperadamente")
                break
                
            if frontend_process and frontend_process.poll() is not None:
                print("❌ Frontend parou inesperadamente")
                break
        
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
        
    except FileNotFoundError:
        print("❌ pnpm não encontrado")
        print("💡 Instale o pnpm: npm install -g pnpm")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        
    finally:
        # Parar processos
        if frontend_process:
            print("🛑 Parando frontend...")
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        if backend_process:
            print("🛑 Parando backend...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
                
        print("✅ Todos os processos foram encerrados")

if __name__ == "__main__":
    main()
