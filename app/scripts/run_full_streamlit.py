#!/usr/bin/env python3
"""
🚀 Agno Teams - Sistema Completo com Streamlit

Executa backend + frontend Streamlit simultaneamente
- Backend: http://localhost:7777 (Teams API)
- Frontend: http://localhost:8501 (Interface Streamlit)

Uso:
python run_full_streamlit.py
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

class AgnoTeamsStreamlitRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def start_backend(self):
        """Inicia o backend em processo separado."""
        print("🚀 Iniciando backend...")
        try:
            # Obter caminho da raiz do projeto (2 níveis acima)
            project_root = Path(__file__).parent.parent.parent
            backend_script = project_root / "app" / "backend" / "agno_teams_playground.py"
            
            self.backend_process = subprocess.Popen(
                [sys.executable, str(backend_script)],
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            print("✅ Backend iniciado (PID: {})".format(self.backend_process.pid))
            
            # Verificar se o processo ainda está rodando
            time.sleep(2)
            if self.backend_process.poll() is not None:
                print("❌ Backend falhou ao iniciar. Verificando saída...")
                output, _ = self.backend_process.communicate()
                if output:
                    print("Saída do backend:")
                    print(output)
                return False
                
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return False
        
        return True
    
    def wait_for_backend(self, max_attempts=30):
        """Aguarda o backend ficar pronto."""
        print("⏳ Aguardando backend ficar pronto...")
        
        for attempt in range(max_attempts):
            try:
                # Verificar se o processo ainda está rodando
                if self.backend_process.poll() is not None:
                    print("❌ Processo do backend morreu")
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
                print(f"⏳ Aguardando backend... (tentativa {attempt+1}/{max_attempts})")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Erro ao verificar backend: {e}")
                time.sleep(2)
        
        print("❌ Timeout aguardando backend ficar pronto")
        return False
    
    def start_frontend(self):
        """Inicia o frontend Streamlit."""
        print("🌐 Iniciando frontend Streamlit...")
        try:
            # Obter caminho da raiz do projeto e do frontend
            project_root = Path(__file__).parent.parent.parent
            frontend_script = project_root / "app" / "frontend" / "streamlit_frontend.py"
            
            self.frontend_process = subprocess.Popen(
                [
                    sys.executable, "-m", "streamlit", "run", 
                    str(frontend_script),
                    "--server.port", "8501",
                    "--server.address", "localhost",
                    "--browser.gatherUsageStats", "false",
                    "--server.headless", "true"
                ],
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Frontend Streamlit iniciado (PID: {})".format(self.frontend_process.pid))
            
        except Exception as e:
            print(f"❌ Erro ao iniciar frontend: {e}")
            self.running = False
            return
    
    def wait_for_frontend(self, max_attempts=20):
        """Aguarda o frontend ficar pronto."""
        print("⏳ Aguardando frontend Streamlit ficar pronto...")
        
        for attempt in range(max_attempts):
            try:
                # Verificar se o processo ainda está rodando
                if self.frontend_process.poll() is not None:
                    print("❌ Processo do frontend morreu")
                    return False
                
                # Verificar se o Streamlit está respondendo
                req = urllib.request.Request("http://localhost:8501")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        print("✅ Frontend Streamlit está pronto!")
                        return True
                        
            except urllib.error.URLError:
                print(f"⏳ Aguardando frontend... (tentativa {attempt+1}/{max_attempts})")
                time.sleep(3)
            except Exception as e:
                print(f"❌ Erro ao verificar frontend: {e}")
                time.sleep(3)
        
        print("❌ Timeout aguardando frontend ficar pronto")
        return False
    
    def cleanup(self):
        """Limpa processos ao encerrar."""
        print("\n🧹 Encerrando processos...")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend encerrado")
            except:
                self.frontend_process.kill()
                print("⚠️ Frontend forçadamente encerrado")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend encerrado")
            except:
                self.backend_process.kill()
                print("⚠️ Backend forçadamente encerrado")
    
    def run(self):
        """Executa o sistema completo."""
        try:
            print("🚀 Agno Teams - Sistema Completo")
            print("=" * 50)
            
            # Iniciar backend
            if not self.start_backend():
                return
            
            # Aguardar backend ficar pronto
            if not self.wait_for_backend():
                return
            
            # Iniciar frontend
            self.start_frontend()
            
            # Aguardar frontend ficar pronto
            if not self.wait_for_frontend():
                return
            
            print("\n🎉 Sistema iniciado com sucesso!")
            print("=" * 50)
            print("🌐 Frontend Streamlit: http://localhost:8501")
            print("🔧 Backend API: http://localhost:7777")
            print("📖 Documentação API: http://localhost:7777/docs")
            print("=" * 50)
            print("Pressione Ctrl+C para encerrar...")
            
            # Manter rodando até interrupção
            while self.running:
                time.sleep(1)
                
                # Verificar se os processos ainda estão rodando
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend parou de funcionar")
                    break
                    
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend parou de funcionar")
                    break
            
        except KeyboardInterrupt:
            print("\n👋 Encerramento solicitado pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro durante execução: {e}")
        finally:
            self.cleanup()

def main():
    """Instala dependências se necessário e executa o sistema."""
    
    # Verificar se streamlit está instalado
    try:
        import streamlit
    except ImportError:
        print("📦 Instalando dependências do Streamlit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Executar sistema
    runner = AgnoTeamsStreamlitRunner()
    
    # Configurar handler para Ctrl+C
    def signal_handler(signum, frame):
        runner.running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    runner.run()

if __name__ == "__main__":
    main()
