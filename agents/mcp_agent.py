from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from config.settings import get_storage_path
from mcp.mcp_tools import MCPTools

def create_mcp_agent() -> Agent:
    """Cria um agente para conexão com serviços MCP."""
    
    # Inicializar ferramentas MCP
    mcp_tools = MCPTools()
    
    return Agent(
        name="MCP Agent",
        model=Gemini(id="gemini-2.0-flash-thinking-exp-01-21"),
        tools=[
            mcp_tools.register_mcp_server,
            mcp_tools.list_mcp_servers,
            mcp_tools.call_mcp_service,
            mcp_tools.check_mcp_health
        ],
        instructions=[
            "Você é um agente especializado em conectar com serviços MCP.",
            "Você tem acesso a ferramentas MCP:",
            "- register_mcp_server: registra um novo servidor MCP",
            "- list_mcp_servers: lista todos os servidores registrados",
            "- call_mcp_service: faz chamadas para serviços MCP",
            "- check_mcp_health: verifica saúde dos servidores",
            "Facilite a comunicação entre diferentes sistemas e protocolos.",
            "Forneça informações sobre conectividade e status dos serviços.",
            "Ajude na configuração e troubleshooting de conexões MCP.",
            "Monitore e reporte sobre a saúde dos serviços conectados."
        ],
        storage=SqliteStorage(
            table_name="mcp_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
