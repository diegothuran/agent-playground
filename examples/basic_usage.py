"""
Exemplo básico de uso do playground Agno.
"""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agno.agent import Agent
from agno.models.google import Gemini
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools

def create_simple_agent():
    """Cria um agente simples para demonstração."""
    return Agent(
        name="Helper Assistant",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é um assistente útil e amigável.",
            "Responda de forma clara e concisa.",
            "Use pesquisas web quando necessário."
        ],
        storage=SqliteStorage(
            table_name="helper_agent", 
            db_file="storage/example_agents.db"
        ),
        markdown=True,
    )

def main():
    """Executa o exemplo básico."""
    print("🚀 Exemplo Básico do Agno Playground")
    print("=" * 40)
    
    # Cria um agente simples
    agent = create_simple_agent()
    
    # Cria o playground
    playground = Playground(agents=[agent])
    
    print(f"✅ Playground criado com o agente: {agent.name}")
    print("🌐 Iniciando servidor em http://localhost:7777")
    print("💡 Experimente fazer perguntas ao assistente!")
    
    # Inicia o servidor
    try:
        app = playground.get_app()
        playground.serve(app, host="localhost", port=7777)
    except KeyboardInterrupt:
        print("\n👋 Exemplo encerrado!")

if __name__ == "__main__":
    main()
