"""
Exemplo de uso avançado do playground Agno.
Este arquivo demonstra como usar recursos avançados e customizações.
"""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agno.agent import Agent
from agno.models.google import Gemini
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from config.settings import get_storage_path
from utils import setup_logging, create_agent_summary

def create_advanced_web_agent():
    """Cria um agente web com configurações avançadas."""
    return Agent(
        name="Advanced Web Researcher",
        model=Gemini(
            id="gemini-1.5-pro",
            temperature=0.7,
            max_output_tokens=2000
        ),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é um pesquisador web especializado e meticuloso.",
            "Sempre verifique múltiplas fontes antes de apresentar informações.",
            "Organize suas pesquisas em seções claras e bem estruturadas.",
            "Inclua links e fontes para todas as informações apresentadas.",
            "Se houver informações conflitantes, mencione isso explicitamente.",
            "Foque em fontes confiáveis e atuais.",
            "Forneça contexto histórico quando relevante."
        ],
        storage=SqliteStorage(
            table_name="advanced_web_agent", 
            db_file=get_storage_path("advanced_agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=10,  # Mais histórico
        markdown=True,
        # Configurações avançadas
        system_prompt="Você é um assistente de pesquisa especializado em análise crítica de informações.",
        auto_save_history=True,
        debug_mode=False
    )

def create_advanced_finance_agent():
    """Cria um agente financeiro com análises avançadas."""
    return Agent(
        name="Quantitative Finance Analyst",
        model=Gemini(
            id="gemini-1.5-pro",
            temperature=0.3,  # Mais conservador para análises financeiras
            max_output_tokens=3000
        ),
        tools=[YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
            historical_data=True,
            financials=True,
            options_data=True
        )],
        instructions=[
            "Você é um analista financeiro quantitativo especializado.",
            "Sempre apresente dados em tabelas bem formatadas.",
            "Inclua análises técnicas e fundamentalistas.",
            "Calcule métricas financeiras relevantes (P/E, ROE, etc.).",
            "Considere fatores macroeconômicos em suas análises.",
            "Sempre mencione riscos e limitações das análises.",
            "Use gráficos e visualizações quando apropriado.",
            "Forneça recomendações baseadas em dados, não especulação."
        ],
        storage=SqliteStorage(
            table_name="advanced_finance_agent", 
            db_file=get_storage_path("advanced_agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=7,
        markdown=True,
        system_prompt="Você é um analista financeiro com 15 anos de experiência em mercados globais."
    )

def create_specialized_agents():
    """Cria agentes especializados para tarefas específicas."""
    
    # Agente para análise de sentimento
    sentiment_agent = Agent(
        name="Sentiment Analysis Expert",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Especialista em análise de sentimento de mercado e opinião pública.",
            "Analise notícias, redes sociais e comunicados para extrair sentimento.",
            "Forneça scores de sentimento quantificados quando possível.",
            "Identifique tendências e mudanças no sentimento ao longo do tempo."
        ],
        storage=SqliteStorage(
            table_name="sentiment_agent", 
            db_file=get_storage_path("specialized_agents.db")
        ),
        add_datetime_to_instructions=True,
        markdown=True
    )
    
    # Agente para comparação de produtos
    comparison_agent = Agent(
        name="Product Comparison Specialist",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Especialista em comparação detalhada de produtos e serviços.",
            "Crie tabelas comparativas com critérios objetivos.",
            "Inclua prós e contras de cada opção.",
            "Considere diferentes perfis de usuário nas recomendações.",
            "Baseie comparações em reviews, especificações e dados confiáveis."
        ],
        storage=SqliteStorage(
            table_name="comparison_agent", 
            db_file=get_storage_path("specialized_agents.db")
        ),
        add_datetime_to_instructions=True,
        markdown=True
    )
    
    return [sentiment_agent, comparison_agent]

def main():
    """Executa o playground com configurações avançadas."""
    
    # Configura logging
    logger = setup_logging("INFO", "logs/advanced_playground.log")
    logger.info("Iniciando playground avançado...")
    
    # Cria agentes avançados
    print("🤖 Criando agentes avançados...")
    
    agents = []
    
    # Agentes principais avançados
    agents.append(create_advanced_web_agent())
    agents.append(create_advanced_finance_agent())
    
    # Agentes especializados
    specialized = create_specialized_agents()
    agents.extend(specialized)
    
    print(f"✅ {len(agents)} agentes criados!")
    
    # Mostra resumo dos agentes
    print("\n📋 Resumo dos agentes:")
    for agent in agents:
        summary = create_agent_summary(agent)
        print(f"  - {summary['name']}: {summary['tools_count']} ferramentas")
    
    # Cria e configura playground
    playground = Playground(
        agents=agents,
        # Configurações avançadas do playground
        # title="Agno Advanced Playground",
        # description="Playground avançado com agentes especializados"
    )
    
    print("\n🚀 Iniciando servidor avançado...")
    print("🌐 Acesse: http://localhost:7777")
    print("💡 Recursos avançados disponíveis!")
    
    try:
        # Corrigindo o método serve para usar a assinatura correta
        app = playground.get_app()
        playground.serve(
            app,
            host="localhost",
            port=7777,
            reload=True
        )
    except KeyboardInterrupt:
        logger.info("Playground encerrado pelo usuário")
        print("\n👋 Playground encerrado!")

if __name__ == "__main__":
    main()
