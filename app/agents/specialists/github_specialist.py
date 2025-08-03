"""
GitHub Specialist - Agente especializado em repositórios GitHub
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from config.settings import get_storage_path

# Importar ferramentas MCP do GitHub se disponível
try:
    from mcp.github_mcp import GitHubMCPTools
    GITHUB_MCP_AVAILABLE = True
except ImportError:
    GITHUB_MCP_AVAILABLE = False

def create_github_specialist() -> Agent:
    """Cria um especialista em GitHub e repositórios."""
    
    tools = []
    tool_instructions = []
    
    if GITHUB_MCP_AVAILABLE:
        import os
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            github_tools = GitHubMCPTools(token=github_token)
            tools.append(github_tools)
            tool_instructions.extend([
                "Ferramentas disponíveis:",
                "- GitHubMCPTools: acesso completo à API do GitHub",
                "  - Buscar repositórios, issues, pull requests",
                "  - Analisar código e histórico de commits",
                "  - Obter estatísticas e métricas de projetos",
                ""
            ])
    
    if not tools:
        tool_instructions.extend([
            "Nota: Ferramentas MCP do GitHub não estão disponíveis.",
            "Forneça orientações baseadas em conhecimento sobre GitHub.",
            ""
        ])
    
    return Agent(
        name="GitHub Specialist",
        role="Expert GitHub and repository analyst",
        model=Gemini(id="gemini-2.0-flash-thinking-exp-01-21"),
        tools=tools,
        instructions=[
            "Você é um especialista em GitHub e gestão de repositórios com expertise em:",
            "- Análise de repositórios e projetos open source",
            "- Workflows de desenvolvimento e CI/CD",
            "- Gestão de issues, pull requests e releases",
            "- Análise de código e histórico de commits",
            "- Métricas de projetos e contribuições",
            "",
            *tool_instructions,
            "Diretrizes:",
            "- Forneça insights sobre qualidade e maturidade de projetos",
            "- Analise padrões de desenvolvimento e colaboração",
            "- Sugira melhorias para workflows e processos",
            "- Identifique tendências e tecnologias em repositórios",
            "- Respeite políticas de privacidade e acesso"
        ],
        storage=SqliteStorage(
            table_name="github_specialist", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
