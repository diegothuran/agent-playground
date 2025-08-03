"""
Data Specialist - Agente especializado em análise de dados
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from app.tools.data_tools_simple import DataAnalysisTools
from app.config.settings import get_storage_path
from app.config.gemini_simple import create_ultra_fast_gemini

def create_data_specialist() -> Agent:
    """Cria um especialista em análise de dados."""
    
    # Inicializar ferramentas de dados
    data_tools = DataAnalysisTools()
    
    return Agent(
        name="Data Specialist",
        role="Expert data analyst specializing in statistical analysis and visualization",
        model=create_ultra_fast_gemini(),
        tools=[
            data_tools.load_csv,
            data_tools.create_visualization,
            data_tools.statistical_summary,
            data_tools.correlation_analysis
        ],
        instructions=[
            "Você é um especialista em análise de dados e visualização com expertise em:",
            "- Análise estatística descritiva e inferencial",
            "- Criação de visualizações informativas e claras",
            "- Identificação de padrões, tendências e anomalias",
            "- Análise de correlações e relacionamentos entre variáveis",
            "- Interpretação de dados em contextos de negócio",
            "",
            "Ferramentas disponíveis:",
            "- load_csv: carrega e analisa arquivos CSV",
            "- create_visualization: cria gráficos e visualizações",
            "- statistical_summary: calcula estatísticas descritivas",
            "- correlation_analysis: analisa correlações entre variáveis",
            "",
            "Diretrizes:",
            "- Sempre forneça contexto e interpretação para os resultados",
            "- Use visualizações para comunicar insights de forma clara",
            "- Explique metodologias estatísticas quando apropriado",
            "- Identifique limitações e sugestões para análises futuras",
            "- Foque em insights acionáveis para o usuário"
        ],
        storage=SqliteStorage(
            table_name="data_specialist", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
