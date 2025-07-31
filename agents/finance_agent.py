from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.tools.yfinance import YFinanceTools
from config.settings import get_storage_path

def create_finance_agent() -> Agent:
    """Cria um agente especializado em análises financeiras."""
    return Agent(
        name="Finance Agent",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[YFinanceTools(
            stock_price=True, 
            analyst_recommendations=True, 
            company_info=True, 
            company_news=True
        )],
        instructions=[
            "Você é um especialista em análises financeiras e mercado de ações.",
            "Sempre use tabelas para exibir dados financeiros de forma organizada.",
            "Inclua análises técnicas e fundamentalistas quando relevante.",
            "Forneça contexto histórico e comparações quando apropriado.",
            "Seja claro sobre riscos e limitações das análises.",
            "Use gráficos e visualizações quando possível."
        ],
        storage=SqliteStorage(
            table_name="finance_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
