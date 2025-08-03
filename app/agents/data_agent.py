from agno.agent import Agent
from agno.models.google import Gemini
from app.config.gemini_simple import create_ultra_fast_gemini
from agno.storage.sqlite import SqliteStorage
from config.settings import get_storage_path
from tools.data_tools import DataAnalysisTools

def create_data_agent() -> Agent:
    """Cria um agente especializado em análise de dados."""
    
    # Inicializar ferramentas de dados
    data_tools = DataAnalysisTools()
    
    return Agent(
        name="Data Analyst",
        model=create_ultra_fast_gemini(),
        tools=[
            data_tools.load_csv,
            data_tools.create_visualization,
            data_tools.statistical_summary,
            data_tools.correlation_analysis
        ],
        instructions=[
            "Você é um especialista em análise de dados e visualização.",
            "Você tem acesso a ferramentas de análise de dados:",
            "- load_csv: carrega e analisa arquivos CSV",
            "- create_visualization: cria gráficos em base64",
            "- statistical_summary: calcula estatísticas descritivas",
            "- correlation_analysis: analisa correlações entre variáveis",
            "Crie visualizações claras e informativas para os dados.",
            "Forneça insights estatísticos relevantes e acionáveis.",
            "Use as ferramentas disponíveis para análises quando apropriado.",
            "Explique metodologias estatísticas utilizadas.",
            "Identifique padrões, tendências e anomalias nos dados."
        ],
        storage=SqliteStorage(
            table_name="data_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=3,
        markdown=True,
    )
