#!/usr/bin/env python3
"""
🚀 Agno Teams - Sistema Completo

Executa backend + frontend simultaneamente
- Backend: http://localhost:7777 (Teams API)
- Frontend: http://localhost:3000 (Interface Web)

Uso:
python run_full.py
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path
from threading import Thread

class AgnoTeamsRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def start_backend(self):
        """Inicia o backend em processo separado."""
        print("🚀 Iniciando backend...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "run_backend.py"],
                cwd=Path(__file__).parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Backend iniciado (PID: {})".format(self.backend_process.pid))
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            
    def start_frontend(self):
        """Inicia o frontend após o backend estar pronto."""
        print("⏱️  Aguardando backend ficar pronto...")
        
        # Aguardar backend ficar disponível
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                import requests
                response = requests.get("http://localhost:7777/v1/playground/status", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("playground") == "available":
                        break
            except:
                pass
            time.sleep(2)
            print(f"🔄 Tentativa {attempt + 1}/{max_attempts}...")
        else:
            print("❌ Backend não ficou disponível a tempo")
            return
            
        print("✅ Backend pronto!")
        print("🎨 Iniciando frontend...")
        
        try:
            frontend_dir = Path(__file__).parent / "frontend"
            if not frontend_dir.exists():
                print(f"❌ Diretório frontend não encontrado: {frontend_dir}")
                return
                
            # Instalar dependências se necessário
            subprocess.run(
                ["pnpm", "install"], 
                cwd=frontend_dir, 
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Iniciar frontend
            self.frontend_process = subprocess.Popen(
                ["pnpm", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Frontend iniciado (PID: {})".format(self.frontend_process.pid))
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar comando: {e}")
        except FileNotFoundError:
            print("❌ pnpm não encontrado")
            print("💡 Instale o pnpm: npm install -g pnpm")
        except Exception as e:
            print(f"❌ Erro ao iniciar frontend: {e}")
    
    def stop_all(self):
        """Para todos os processos."""
        self.running = False
        
        if self.frontend_process:
            print("🛑 Parando frontend...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
        
        if self.backend_process:
            print("🛑 Parando backend...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                
        print("✅ Todos os processos foram encerrados")
    
    def run(self):
        """Executa o sistema completo."""
        print("🚀 Agno Teams - Sistema Completo")
        print("=" * 50)
        
        try:
            # Iniciar backend
            self.start_backend()
            time.sleep(2)
            
            # Iniciar frontend em thread separada
            frontend_thread = Thread(target=self.start_frontend)
            frontend_thread.start()
            
            # Aguardar tudo estar pronto
            frontend_thread.join()
            
            if self.running:
                print("\n🎉 Sistema completo iniciado!")
                print("=" * 50)
                print("🌐 Frontend: http://localhost:3000")
                print("🔗 Backend API: http://localhost:7777")
                print("📖 Documentação: http://localhost:7777/docs")
                print("=" * 50)
                print("⌨️  Pressione Ctrl+C para parar")
                
                # Manter rodando até Ctrl+C
                while self.running:
                    time.sleep(1)
                    
                    # Verificar se processos ainda estão rodando
                    if self.backend_process and self.backend_process.poll() is not None:
                        print("❌ Backend parou inesperadamente")
                        break
                        
                    if self.frontend_process and self.frontend_process.poll() is not None:
                        print("❌ Frontend parou inesperadamente")
                        break
        
        except KeyboardInterrupt:
            print("\n👋 Sistema encerrado pelo usuário")
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            self.stop_all()

def signal_handler(signum, frame):
    """Handler para sinais do sistema."""
    print("\n🛑 Recebido sinal de parada...")
    runner.stop_all()
    sys.exit(0)

if __name__ == "__main__":
    runner = AgnoTeamsRunner()
    
    # Configurar handlers para parada graciosa
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    runner.run()
