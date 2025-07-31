"""
Exemplo de conversas entre múltiplos agentes no playground Agno.
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

def create_researcher_agent():
    """Cria um agente especializado em pesquisa."""
    return Agent(
        name="Research Specialist",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é um especialista em pesquisa e análise de informações.",
            "Sua função é buscar e analisar dados de fontes confiáveis.",
            "Sempre cite suas fontes e seja preciso nas informações.",
            "Colabore com outros agentes fornecendo dados relevantes."
        ],
        storage=SqliteStorage(
            table_name="researcher_agent", 
            db_file="storage/multi_agent_example.db"
        ),
        markdown=True,
    )

def create_analyst_agent():
    """Cria um agente especializado em análise."""
    return Agent(
        name="Data Analyst",
        model=Gemini(id="gemini-1.5-pro"),
        instructions=[
            "Você é um analista de dados especializado.",
            "Sua função é analisar informações fornecidas por outros agentes.",
            "Identifique padrões, tendências e insights importantes.",
            "Forneça conclusões baseadas em evidências."
        ],
        storage=SqliteStorage(
            table_name="analyst_agent", 
            db_file="storage/multi_agent_example.db"
        ),
        markdown=True,
    )

def create_writer_agent():
    """Cria um agente especializado em escrita."""
    return Agent(
        name="Content Writer",
        model=Gemini(id="gemini-1.5-pro"),
        instructions=[
            "Você é um escritor especializado em conteúdo técnico.",
            "Sua função é criar relatórios e documentos bem estruturados.",
            "Use as informações fornecidas por outros agentes.",
            "Escreva de forma clara, objetiva e profissional."
        ],
        storage=SqliteStorage(
            table_name="writer_agent", 
            db_file="storage/multi_agent_example.db"
        ),
        markdown=True,
    )

def main():
    """Executa o exemplo de múltiplos agentes."""
    print("🤖 Exemplo Multi-Agente do Agno Playground")
    print("=" * 45)
    
    # Cria os agentes especializados
    researcher = create_researcher_agent()
    analyst = create_analyst_agent()
    writer = create_writer_agent()
    
    # Cria o playground com múltiplos agentes
    playground = Playground(agents=[researcher, analyst, writer])
    
    print(f"✅ Playground criado com {len(playground.agents)} agentes:")
    for agent in playground.agents:
        print(f"   • {agent.name}")
    
    print("\n🌐 Iniciando servidor em http://localhost:7778")
    print("💡 Experimente fazer uma pesquisa complexa que requeira colaboração!")
    print("💡 Exemplo: 'Pesquise sobre IA generativa, analise os dados e crie um relatório'")
    
    # Inicia o servidor
    try:
        app = playground.get_app()
        playground.serve(app, host="localhost", port=7778)
    except KeyboardInterrupt:
        print("\n👋 Exemplo encerrado!")

if __name__ == "__main__":
    main()
