"""
Web Specialist - Agente especializado em pesquisa web
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from config.settings import get_storage_path

def create_web_specialist() -> Agent:
    """Cria um especialista em pesquisa web."""
    
    return Agent(
        name="Web Specialist",
        role="Expert web researcher and information gatherer",
        model=Gemini(id="gemini-2.0-flash-thinking-exp-01-21"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é um especialista em pesquisa web e coleta de informações com expertise em:",
            "- Pesquisa eficiente e estratégica na web",
            "- Verificação e validação de fontes",
            "- Síntese de informações de múltiplas fontes",
            "- Identificação de tendências e notícias atuais",
            "- Análise de conteúdo e credibilidade",
            "",
            "Ferramentas disponíveis:",
            "- DuckDuckGoTools: pesquisa web abrangente e atualizada",
            "",
            "Diretrizes:",
            "- Sempre cite fontes e forneça links quando possível",
            "- Verifique informações em múltiplas fontes confiáveis",
            "- Priorize fontes oficiais e reconhecidas",
            "- Organize informações de forma clara e estruturada",
            "- Indique quando informações são preliminares ou não verificadas",
            "- Forneça contexto temporal relevante"
        ],
        storage=SqliteStorage(
            table_name="web_specialist", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
