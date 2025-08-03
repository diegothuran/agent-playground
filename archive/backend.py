#!/usr/bin/env python3
"""
Agno Teams Playground - Sistema moderno de agentes especializados

Este playground implementa a arquitetura avançada de Teams do Agno com:
- Route Mode: Team principal que direciona para especialistas
- Coordinate Mode: Teams que coordenam múltiplos agentes  
- Collaborate Mode: Teams colaborativos
- Interface web via Agno Playground
- Memória persistente e histórico de sessões

Uso:
python agno_teams_playground.py

Baseado na documentação oficial: https://docs.agno.com/teams/introduction
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

import agno.agent
import agno.team
import agno.models.google
import agno.playground
import agno.storage.sqlite

# Importar classes específicas
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage

# Tentar importar memória v2, caso não exista usar básica
try:
    from agno.memory.v2.db.sqlite import SqliteMemoryDb
    from agno.memory.v2.memory import Memory
    MEMORY_V2_AVAILABLE = True
except ImportError:
    try:
        from agno.memory.db.sqlite import SqliteMemoryDb
        from agno.memory.memory import Memory
        MEMORY_V2_AVAILABLE = False
    except ImportError:
        # Sem memória persistente disponível
        SqliteMemoryDb = None
        Memory = None
        MEMORY_V2_AVAILABLE = False

# Importar especialistas
from agents.specialists.data_specialist import create_data_specialist
from agents.specialists.code_specialist import create_code_specialist
from agents.specialists.finance_specialist import create_finance_specialist
from agents.specialists.web_specialist import create_web_specialist
from agents.specialists.github_specialist import create_github_specialist

from config.settings import get_storage_path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgnoTeamsPlayground:
    """Playground moderno para Teams do Agno com interface web."""
    
    def __init__(self, port: int = 7777, enable_memory: bool = True):
        self.port = port
        self.enable_memory = enable_memory
        
        # Verificar API key
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY não encontrada. "
                "Configure no arquivo .env: GOOGLE_API_KEY=sua_api_key_aqui"
            )
        
        # Configurar modelo padrão - Gemini 2.0 Flash
        self.default_model = Gemini(id="gemini-2.0-flash-thinking-exp-01-21", api_key=self.api_key)
        
        # Configurar memória persistente
        if self.enable_memory:
            self.memory_db = SqliteMemoryDb(
                table_name="teams_memory", 
                db_file=get_storage_path("teams_memory.db")
            )
            self.memory = Memory(db=self.memory_db)
        else:
            self.memory = None
            
        self.teams = {}
        self.playground = None
        
    def create_specialists(self) -> List[Agent]:
        """Cria todos os agentes especialistas."""
        specialists = []
        
        try:
            # Data Specialist
            data_specialist = create_data_specialist()
            data_specialist.model = self.default_model
            if self.memory:
                data_specialist.memory = self.memory
            specialists.append(data_specialist)
            
            # Code Specialist
            code_specialist = create_code_specialist()
            code_specialist.model = self.default_model
            if self.memory:
                code_specialist.memory = self.memory
            specialists.append(code_specialist)
            
            # Finance Specialist
            finance_specialist = create_finance_specialist()
            finance_specialist.model = self.default_model
            if self.memory:
                finance_specialist.memory = self.memory
            specialists.append(finance_specialist)
            
            # Web Specialist
            web_specialist = create_web_specialist()
            web_specialist.model = self.default_model
            if self.memory:
                web_specialist.memory = self.memory
            specialists.append(web_specialist)
            
            # GitHub Specialist
            github_specialist = create_github_specialist()
            github_specialist.model = self.default_model
            if self.memory:
                github_specialist.memory = self.memory
            specialists.append(github_specialist)
            
            logger.info(f"✅ {len(specialists)} especialistas criados com sucesso!")
            return specialists
            
        except Exception as e:
            logger.error(f"Erro ao criar especialistas: {e}")
            raise
    
    def create_main_team_leader(self, specialists: List[Agent]) -> Team:
        """Cria o Team Leader principal que implementa o fluxo completo."""
        
        config = {
            "name": "🧠 Agno Teams Leader",
            "members": specialists,  # Usar 'members' em vez de 'agents'
            "model": self.default_model,
            "description": """Team Leader inteligente powered by Gemini 2.0 Flash que analisa o contexto da pergunta e decide:
            
🔍 **Análise de Contexto**: Compreende a natureza e complexidade da solicitação
📍 **Route Mode**: Para tarefas simples, direciona para o especialista mais adequado
🔄 **Coordinate Mode**: Para tarefas complexas, orquestra múltiplos agentes em pipeline
🤝 **Collaborate Mode**: Para análises abrangentes, todos os especialistas trabalham juntos
            
Especialistas disponíveis (todos powered by Gemini 2.0 Flash):
💰 Finance Agent - Análise financeira e mercados
🌐 Web Research Agent - Pesquisa web e informações online  
💻 Code Analysis Agent - Análise e desenvolvimento de código
📊 Data Analysis Agent - Análise estatística e visualizações
🐙 GitHub Agent - Integração e análise de repositórios GitHub""",
            "show_members_responses": True,
            "markdown": True,
            "instructions": [
                "Você é o Team Leader do Agno Teams, responsável por:",
                "",
                "1. 🔍 **ANÁLISE DE CONTEXTO**:",
                "   - Analise a pergunta do usuário semanticamente",
                "   - Identifique o domínio principal (finanças, código, dados, web, github)",
                "   - Determine a complexidade da tarefa",
                "",
                "2. 📊 **DECISÃO DE MODO**:",
                "   - **Route Mode**: Tarefas simples → direcionar para 1 especialista",
                "   - **Coordinate Mode**: Tarefas complexas → orquestrar múltiplos agentes",
                "   - **Collaborate Mode**: Análises abrangentes → todos trabalham juntos",
                "",
                "3. 🎯 **EXECUÇÃO INTELIGENTE**:",
                "   - Route: Selecione o especialista mais adequado",
                "   - Coordinate: Crie pipeline eficiente de agentes",
                "   - Collaborate: Facilite colaboração entre todos",
                "",
                "4. 🧠 **SÍNTESE & RESPOSTA**:",
                "   - Compile resultados de múltiplas fontes quando necessário",
                "   - Forneça resposta contextualizada e acionável",
                "   - Capture feedback para aprendizado contínuo",
                "",
                "**ESPECIALISTAS DISPONÍVEIS:**",
                "• Finance Agent: yfinance, análise de mercados, indicadores financeiros",
                "• Web Agent: pesquisa web, scraping, informações online",
                "• Code Agent: análise de código, debugging, boas práticas",
                "• Data Agent: pandas, visualizações, estatísticas",
                "• GitHub Agent: repositórios, commits, análise de código no GitHub",
                "",
                "Sempre explique sua decisão de modo e como está orquestrando os agentes."
            ]
        }
        
        if self.memory:
            config.update({
                "memory": self.memory,
                "enable_agentic_memory": True,
            })
            
        config.update({
            "add_history_to_messages": True,
            "num_history_runs": 5,
            "enable_session_summaries": True,
        })
        
        return Team(**config)
    
    def create_playground(self) -> Playground:
        """Cria o playground web com o Team Leader principal."""
        
        try:
            # Criar especialistas
            specialists = self.create_specialists()
            
            # Criar o Team Leader principal que gerencia tudo
            main_team = self.create_main_team_leader(specialists)
            
            # O frontend espera agents, então vamos expor o team como agent
            self.playground = Playground(
                agents=[main_team],  # Expor team como agent para compatibilidade com frontend
                name="Agno Teams Playground",
                description="Sistema inteligente de agentes especializados com Team Leader"
            )
            
            print(f"🌐 Playground criado com Team Leader principal")
            print(f"👥 {len(specialists)} especialistas disponíveis no team")
            print(f"📡 Servidor será iniciado na porta {self.port}")
            
            return self.playground
            
        except Exception as e:
            logger.error(f"Erro ao criar playground: {e}")
            raise
    
    def run(self):
        """Inicia o playground web."""
        
        try:
            if not self.playground:
                self.create_playground()
            
            print(f"\n🎮 Agno Teams Playground")
            print(f"=" * 50)
            print(f"🌐 Interface Web: http://localhost:{self.port}")
            print(f"🧠 Team Leader: Análise inteligente de contexto")
            print(f"📋 Modos disponíveis:")
            print(f"   📍 Route Mode: Tarefas simples → 1 especialista")
            print(f"   🔄 Coordinate Mode: Tarefas complexas → múltiplos agentes")
            print(f"   🤝 Collaborate Mode: Análises abrangentes → todos juntos")
            print(f"👥 Especialistas: Finance, Web, Code, Data, GitHub")
            print(f"=" * 50)
            print(f"🚀 Iniciando servidor...")
            
            # Servir o playground
            app = self.playground.get_app()
            self.playground.serve(
                app,
                port=self.port,
                host="0.0.0.0"
            )
            
        except KeyboardInterrupt:
            print("\n👋 Playground encerrado pelo usuário")
        except Exception as e:
            logger.error(f"Erro ao executar playground: {e}")
            raise

def main():
    """Função principal."""
    
    try:
        # Verificar dependências
        print("🔍 Verificando configuração...")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY não encontrada!")
            print("Configure no arquivo .env:")
            print("GOOGLE_API_KEY=sua_api_key_aqui")
            print("📝 Use o arquivo .env.example como modelo")
            return
            
        print("✅ Configuração OK!")
        print(f"🔑 API Key configurada: {api_key[:10]}...")
        
        # Criar e executar playground
        print("🎮 Criando playground...")
        playground = AgnoTeamsPlayground(port=7777)
        print("🚀 Iniciando playground...")
        playground.run()
        
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
