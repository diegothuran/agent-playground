"""
Agente especializado para GitHub MCP
"""
from agno.agent import Agent
from agno.models.google import Gemini
from app.config.gemini_simple import create_ultra_fast_gemini
from agno.storage.sqlite import SqliteStorage
from config.settings import get_storage_path
from mcp.github_mcp import GitHubMCPTools
import os


def create_github_agent() -> Agent:
    """Cria um agente especializado para integração com GitHub."""
    
    # Obter token do GitHub das variáveis de ambiente
    github_token = os.getenv("GITHUB_TOKEN")
    
    # Inicializar ferramentas GitHub MCP
    github_tools = GitHubMCPTools(token=github_token)
    
    return Agent(
        name="GitHub Agent",
        model=create_ultra_fast_gemini(),
        tools=[
            github_tools.search_repositories,
            github_tools.get_repository_info,
            github_tools.get_repository_issues,
            github_tools.get_user_info
        ],
        instructions=[
            "Você é um agente especializado em interagir com a API do GitHub via MCP.",
            "",
            "🔍 BUSCA DE REPOSITÓRIOS:",
            "- Use search_repositories para encontrar repositórios por palavras-chave",
            "- Filtre por linguagem, estrelas, ou outros critérios",
            "- Forneça resultados organizados e relevantes",
            "",
            "📊 INFORMAÇÕES DE REPOSITÓRIOS:",
            "- Use get_repository_info para detalhes completos de um repo",
            "- Inclua estatísticas, linguagens, tópicos, e metadados",
            "- Forneça links úteis e informações de uso",
            "",
            "🐛 ISSUES E PROBLEMAS:",
            "- Use get_repository_issues para listar issues abertas/fechadas",
            "- Filtre por estado, labels, ou autor",
            "- Ajude a entender o status do projeto",
            "",
            "👤 INFORMAÇÕES DE USUÁRIOS:",
            "- Use get_user_info para perfis de desenvolvedores",
            "- Forneça estatísticas e informações públicas",
            "- Respeite privacidade e políticas do GitHub",
            "",
            "🎯 MELHORES PRÁTICAS:",
            "- Sempre forneça links diretos para recursos",
            "- Organize informações em tabelas quando apropriado",
            "- Sugira próximos passos ou ações relacionadas",
            "- Respeite limites de rate da API do GitHub"
        ],
        storage=SqliteStorage(
            table_name="github_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
