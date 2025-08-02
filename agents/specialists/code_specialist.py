"""
Code Specialist - Agente especializado em análise e desenvolvimento de código
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from tools.code_tools import CodeAnalysisTools
from config.settings import get_storage_path

def create_code_specialist() -> Agent:
    """Cria um especialista em código e desenvolvimento."""
    
    # Inicializar ferramentas de código
    code_tools = CodeAnalysisTools()
    
    return Agent(
        name="Code Specialist", 
        role="Expert software developer and code analyst",
        model=Gemini(id="gemini-2.0-flash-thinking-exp-01-21"),
        tools=[
            code_tools.analyze_python_file,
            code_tools.check_code_style,
            code_tools.generate_docstring
        ],
        instructions=[
            "Você é um especialista em desenvolvimento de software com expertise em:",
            "- Análise de estrutura de código Python",
            "- Verificação de estilo e boas práticas",
            "- Geração de documentação e docstrings",
            "- Identificação de classes, funções e imports",
            "",
            "Ferramentas disponíveis:",
            "- analyze_python_file: analisa estrutura de arquivos Python",
            "- check_code_style: verifica estilo usando flake8",
            "- generate_docstring: gera docstrings para funções",
            "",
            "Diretrizes:",
            "- Sempre analise a estrutura antes de fazer sugestões",
            "- Use verificação de estilo para identificar problemas",
            "- Gere documentação clara e útil",
            "- Foque em melhorias práticas e implementáveis"
        ],
        storage=SqliteStorage(
            table_name="code_specialist", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
