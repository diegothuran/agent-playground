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
import urllib.request
import urllib.error
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
            # Iniciar com output capturado para debug
            self.backend_process = subprocess.Popen(
                [sys.executable, "run_backend.py"],
                cwd=Path(__file__).parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Redirecionar stderr para stdout
                universal_newlines=True,
                bufsize=1
            )
            print("✅ Backend iniciado (PID: {})".format(self.backend_process.pid))
            
            # Aguardar um pouco e verificar se o processo ainda está rodando
            time.sleep(2)
            if self.backend_process.poll() is not None:
                print("❌ Backend falhou ao iniciar. Verificando saída...")
                # Ler toda a saída disponível
                output, _ = self.backend_process.communicate()
                if output:
                    print("Saída do backend:")
                    print(output)
                return False
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return False
            
    def wait_for_backend(self):
        """Aguarda o backend estar pronto."""
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # Verificar se o processo ainda está rodando
                if self.backend_process.poll() is not None:
                    print(f"❌ Backend morreu (exit code: {self.backend_process.returncode})")
                    # Tentar ler saída do processo morto
                    try:
                        output, _ = self.backend_process.communicate(timeout=1)
                        if output:
                            print("Última saída do backend:")
                            print(output)
                    except:
                        pass
                    return False
                
                # Verificar se o endpoint está respondendo
                req = urllib.request.Request("http://localhost:7777/v1/playground/status")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        print("✅ Backend está pronto!")
                        return True
                        
            except urllib.error.URLError as e:
                attempt += 1
                print(f"⏳ Aguardando backend... (tentativa {attempt}/{max_attempts})")
                if hasattr(e, 'reason'):
                    print(f"   Razão: {e.reason}")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Erro ao verificar backend: {e}")
                attempt += 1
                time.sleep(2)
        
        print("❌ Timeout aguardando backend ficar pronto")
        return False
    
    def start_frontend(self):
        """Inicia o frontend em processo separado."""
        print("🌐 Iniciando frontend...")
        try:
            frontend_dir = Path(__file__).parent / "frontend"
            
            if not frontend_dir.exists():
                print("❌ Diretório frontend não encontrado")
                self.running = False
                return
            
            # Verificar se node_modules existe
            if not (frontend_dir / "node_modules").exists():
                print("📦 Instalando dependências do frontend...")
                install_process = subprocess.run(
                    ["pnpm", "install"],
                    cwd=frontend_dir,
                    capture_output=True,
                    text=True
                )
                if install_process.returncode != 0:
                    print(f"❌ Erro ao instalar dependências: {install_process.stderr}")
                    self.running = False
                    return
            
            # Aguardar backend estar pronto
            if not self.wait_for_backend():
                print("❌ Backend não ficou pronto")
                self.running = False
                return
            
            # Iniciar frontend
            self.frontend_process = subprocess.Popen(
                ["pnpm", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Frontend iniciado (PID: {})".format(self.frontend_process.pid))
            
        except Exception as e:
            print(f"❌ Erro ao iniciar frontend: {e}")
            self.running = False
    
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
