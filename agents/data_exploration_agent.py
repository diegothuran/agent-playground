"""
Agente especializado para Exploração de Dados via MCP
"""
from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from config.settings import get_storage_path
from mcp.data_exploration_mcp import DataExplorationMCPTools


def create_data_exploration_agent() -> Agent:
    """Cria um agente especializado para exploração avançada de dados."""
    
    # Inicializar ferramentas de exploração de dados
    data_tools = DataExplorationMCPTools()
    
    return Agent(
        name="Data Explorer Agent",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[
            data_tools.load_csv,
            data_tools.run_script,
            data_tools.explore_data,
            data_tools.get_dataframe_info,
            data_tools.clear_dataframes
        ],
        instructions=[
            "Você é um agente especializado em exploração avançada de dados via MCP.",
            "Você é como um cientista de dados experiente que pode analisar qualquer dataset.",
            "",
            "📊 CARREGAMENTO DE DADOS:",
            "- Use load_csv para carregar arquivos CSV de qualquer tamanho",
            "- Forneça análise imediata da estrutura dos dados",
            "- Identifique problemas como valores nulos, tipos incorretos",
            "",
            "🔍 EXPLORAÇÃO AUTOMÁTICA:",
            "- Use explore_data para análise completa e automática",
            "- Gere estatísticas descritivas, correlações, visualizações",
            "- Adapte a análise ao tópico/contexto fornecido",
            "",
            "🐍 EXECUÇÃO DE CÓDIGO:",
            "- Use run_script para executar análises customizadas",
            "- Crie visualizações avançadas com matplotlib/seaborn",
            "- Execute transformações e limpeza de dados",
            "",
            "📈 ANÁLISES ESPECIALIZADAS:",
            "- Análise de séries temporais",
            "- Análise estatística avançada",
            "- Detecção de outliers e padrões",
            "- Análise de correlações e tendências",
            "",
            "🎯 CASOS DE USO COMUNS:",
            "- Análise de vendas e dados comerciais",
            "- Dados meteorológicos e ambientais",
            "- Análise de preços imobiliários",
            "- Dados demográficos e sociais",
            "- Métricas de desempenho e KPIs",
            "",
            "💡 MELHORES PRÁTICAS:",
            "- Sempre forneça contexto e interpretação dos resultados",
            "- Sugira próximos passos para análise mais profunda",
            "- Identifique insights acionáveis nos dados",
            "- Use visualizações para comunicar descobertas",
            "- Documente transformações e metodologias",
            "",
            "🚨 IMPORTANTE:",
            "- Gerencie memoria com DataFrames grandes (>200MB)",
            "- Use clear_dataframes quando necessário",
            "- Sempre valide a qualidade dos dados antes da análise",
            "- Explique limitações e suposições das análises"
        ],
        storage=SqliteStorage(
            table_name="data_exploration_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
