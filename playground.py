import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agno.playground import Playground
from config.settings import load_config, validate_config, get_storage_path
from agents.web_agent import create_web_agent
from agents.finance_agent import create_finance_agent
from agents.code_agent import create_code_agent
from agents.data_agent import create_data_agent
from agents.mcp_agent import create_mcp_agent

def create_playground():
    """Cria e configura o playground com todos os agentes."""
    
    # Valida configurações
    if not validate_config():
        print("❌ Erro na validação das configurações. Verifique o arquivo .env")
        return None
    
    config = load_config()
    
    # Cria diretórios necessários
    os.makedirs(config["storage_dir"], exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    print("🚀 Criando agentes...")
    
    # Cria os agentes
    agents = []
    
    try:
        # Agente Web
        web_agent = create_web_agent()
        agents.append(web_agent)
        print("✅ Web Agent criado")
        
        # Agente Financeiro
        finance_agent = create_finance_agent()
        agents.append(finance_agent)
        print("✅ Finance Agent criado")
        
        # Agente de Código
        code_agent = create_code_agent()
        agents.append(code_agent)
        print("✅ Code Agent criado")
        
        # Agente de Dados
        data_agent = create_data_agent()
        agents.append(data_agent)
        print("✅ Data Agent criado")
        
        # Agente MCP
        mcp_agent = create_mcp_agent()
        agents.append(mcp_agent)
        print("✅ MCP Agent criado")
        
    except Exception as e:
        print(f"❌ Erro ao criar agentes: {str(e)}")
        print("Verifique se todas as dependências estão instaladas corretamente.")
        return None
    
    # Cria o playground com lista de agentes
    playground = Playground(agents=agents)
    
    print(f"🎮 Playground criado com {len(agents)} agentes!")
    print("📋 Agentes disponíveis:")
    for agent in agents:
        print(f"  - {agent.name}")
    
    return playground

def main():
    """Função principal para executar o playground."""
    print("🎯 Iniciando Agno Playground...")
    print("=" * 50)
    
    playground = create_playground()
    
    if playground is None:
        print("❌ Falha ao criar o playground. Encerrando...")
        return
    
    config = load_config()
    
    print(f"🌐 Iniciando servidor em http://{config['host']}:{config['port']}")
    print("💡 Dica: Pressione Ctrl+C para parar o servidor")
    print("=" * 50)
    
    try:
        # Inicia o servidor usando o método correto do Agno Playground
        # O método serve() precisa do app como primeiro parâmetro
        app = playground.get_app()
        playground.serve(
            app,
            port=config["port"],
            host=config["host"]
        )
    except KeyboardInterrupt:
        print("\n👋 Playground encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar o playground: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
