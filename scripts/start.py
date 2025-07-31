#!/usr/bin/env python3
"""
Script de inicialização rápida para o Agno Playground.
Este script verifica dependências e inicia o playground.
"""

import os
import sys
import subprocess

def check_python_version():
    """Verifica se a versão do Python é adequada."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def check_env_file():
    """Verifica se o arquivo .env existe."""
    if not os.path.exists(".env"):
        print("❌ Arquivo .env não encontrado")
        print("💡 Execute: cp .env.example .env")
        print("💡 Configure sua OPENAI_API_KEY no arquivo .env")
        return False
    print("✅ Arquivo .env encontrado")
    return True

def check_venv():
    """Verifica se o ambiente virtual existe."""
    if not os.path.exists("venv"):
        print("❌ Ambiente virtual não encontrado")
        print("💡 Execute: python -m venv venv")
        return False
    print("✅ Ambiente virtual encontrado")
    return True

def install_dependencies():
    """Instala as dependências básicas."""
    print("📦 Instalando dependências básicas...")
    
    basic_deps = [
        "python-dotenv",
        "google-genai",
        "requests",
        "fastapi",
        "uvicorn"
    ]
    
    for dep in basic_deps:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], check=True, capture_output=True)
            print(f"✅ {dep} instalado")
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao instalar {dep}")
            return False
    
    return True

def start_simple_playground():
    """Inicia um playground simplificado."""
    print("🚀 Iniciando playground simplificado...")
    
    # Código de um playground mínimo
    playground_code = '''
import os
from dotenv import load_dotenv

load_dotenv()

# Verifica se a chave do Google está configurada
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ GOOGLE_API_KEY não configurada no arquivo .env")
    exit(1)

try:
    from agno.agent import Agent
    from agno.models.google import Gemini
    from agno.playground import Playground
    from agno.storage.sqlite import SqliteStorage
    from agno.tools.duckduckgo import DuckDuckGoTools
    
    # Cria agente simples
    agent = Agent(
        name="Simple Assistant",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DuckDuckGoTools()],
        instructions=["Você é um assistente útil e amigável."],
        storage=SqliteStorage(table_name="simple_agent", db_file="storage/agents.db"),
        markdown=True,
    )
    
    # Cria playground
    playground = Playground(agents=[agent])
    
    print("✅ Playground iniciado!")
    print("🌐 Acesse: http://localhost:7777")
    
    playground.serve(host="localhost", port=7777, reload=True)
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Instale o agno: pip install agno")
except Exception as e:
    print(f"❌ Erro: {e}")
'''
    
    # Executa o código do playground
    exec(playground_code)

def main():
    """Função principal."""
    print("🎯 Agno Playground - Inicialização Rápida")
    print("=" * 50)
    
    # Verificações básicas
    if not check_python_version():
        return
    
    if not check_env_file():
        return
    
    # Cria diretórios necessários
    os.makedirs("storage", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Tenta instalar dependências básicas
    print("🔄 Verificando dependências...")
    install_dependencies()
    
    # Inicia o playground
    try:
        start_simple_playground()
    except KeyboardInterrupt:
        print("\\n👋 Playground encerrado!")
    except Exception as e:
        print(f"❌ Erro ao iniciar playground: {e}")
        print("💡 Tente executar: python playground.py")

if __name__ == "__main__":
    main()
