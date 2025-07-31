import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agno.playground import Playground
from config.settings import load_config, validate_config
from agents.orchestrator_agent import create_orchestrator_agent

def create_orchestrated_playground():
    """Cria e configura o playground com o agente orquestrador."""
    
    # Valida configurações
    if not validate_config():
        print("❌ Erro na validação das configurações. Verifique o arquivo .env")
        return None
    
    config = load_config()
    
    # Cria diretórios necessários
    os.makedirs(config["storage_dir"], exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    print("🎯 Criando Agente Orquestrador...")
    
    try:
        # Cria o agente orquestrador
        orchestrator = create_orchestrator_agent()
        
        # Renomeia o orquestrador para não mostrar que é um orquestrador
        orchestrator.name = "Assistente IA"
        
        print("✅ Assistente IA criado com sucesso!")
        print("🤖 Seleção automática e inteligente de especialistas ativada")
        
    except Exception as e:
        print(f"❌ Erro ao criar assistente: {str(e)}")
        print("Verifique se todas as dependências estão instaladas corretamente.")
        import traceback
        traceback.print_exc()
        return None
    
    # Cria o playground com o orquestrador (mas aparece como um assistente único)
    playground = Playground(agents=[orchestrator])
    
    print("🎮 Playground Inteligente criado!")
    print("🧠 Experiência unificada: Um assistente, múltiplas especialidades")
    
    return playground

def main():
    """Função principal para executar o playground orquestrado."""
    print("🎯 Iniciando Agno Playground com Orquestrador Inteligente...")
    print("=" * 60)
    
    playground = create_orchestrated_playground()
    
    if playground is None:
        print("❌ Falha ao criar o playground. Encerrando...")
        return
    
    config = load_config()
    
    print(f"🌐 Iniciando servidor em http://{config['host']}:{config['port']}")
    print("🎨 Frontend disponível em http://localhost:3000")
    print("🧠 Orquestrador Ativo: Decisão automática de agentes")
    print("💡 Dica: Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    
    try:
        # Inicia o servidor usando o método correto do Agno Playground
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
