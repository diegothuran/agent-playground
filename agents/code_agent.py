from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from config.settings import get_storage_path
from tools.code_tools import CodeAnalysisTools

def create_code_agent() -> Agent:
    """Cria um agente especializado em análise e geração de código."""
    
    # Inicializar ferramentas de código
    code_tools = CodeAnalysisTools()
    
    return Agent(
        name="Code Assistant",
        model=Gemini(id="gemini-2.0-flash-thinking-exp-01-21"),
        tools=[
            code_tools.analyze_python_file,
            code_tools.check_code_style,
            code_tools.generate_docstring
        ],
        instructions=[
            "Você é um assistente especializado em programação e desenvolvimento.",
            "Você tem acesso a ferramentas de análise de código:",
            "- analyze_python_file: analisa estrutura de arquivos Python",
            "- check_code_style: verifica estilo com flake8",
            "- generate_docstring: gera documentação para funções",
            "Analise código de forma detalhada e forneça sugestões de melhoria.",
            "Explique conceitos de programação de forma clara e didática.",
            "Sempre inclua exemplos práticos quando apropriado.",
            "Siga as melhores práticas de desenvolvimento para cada linguagem.",
            "Forneça código limpo, bem documentado e testável."
        ],
        storage=SqliteStorage(
            table_name="code_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=3,
        markdown=True,
    )
