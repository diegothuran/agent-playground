from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from config.settings import get_storage_path

def create_web_agent() -> Agent:
    """Cria um agente especializado em pesquisas web."""
    return Agent(
        name="Web Search Agent",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é um especialista em pesquisas na web.",
            "Sempre inclua as fontes das informações encontradas.",
            "Forneça resumos claros e objetivos.",
            "Se necessário, faça múltiplas pesquisas para obter informações completas.",
            "Organize as informações de forma estruturada e fácil de ler."
        ],
        storage=SqliteStorage(
            table_name="web_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
