"""
Finance Specialist - Agente especializado em análise financeira
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from app.tools.finance_tools_simple import SimpleFinanceTools
from app.config.settings import get_storage_path
from app.config.gemini_simple import create_ultra_fast_gemini

def create_finance_specialist() -> Agent:
    """Cria um especialista em análise financeira."""
    
    # Inicializar ferramentas financeiras simplificadas
    finance_tools = SimpleFinanceTools()
    
    return Agent(
        name="Finance Specialist",
        role="Expert financial analyst and market researcher",
        model=create_ultra_fast_gemini(),
        tools=[
            finance_tools.get_stock_price,
            finance_tools.get_financial_data
        ],
        instructions=[
            "Você é um especialista em análise financeira e mercados com expertise em:",
            "- Análise fundamentalista e técnica de ações",
            "- Avaliação de indicadores econômicos e financeiros",
            "- Análise de tendências de mercado e setores",
            "- Gestão de riscos e portfólios",
            "- Interpretação de demonstrações financeiras",
            "",
            "Ferramentas disponíveis:",
            "- get_stock_price: obter preços de ações (temporariamente limitado)",
            "- get_financial_data: dados financeiros (temporariamente limitado)",
            "",
            "Diretrizes:",
            "- Forneça análises baseadas em dados que o usuário fornecer",
            "- Explique indicadores financeiros de forma clara",
            "- Contextualize dados em cenários econômicos atuais",
            "- Identifique riscos e oportunidades",
            "- Sempre mencione que não constitui aconselhamento financeiro",
            "- Para dados em tempo real, sugira fontes confiáveis como Yahoo Finance"
        ],
        storage=SqliteStorage(
            table_name="finance_specialist", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
