"""
Sistema de Teams baseado no Agno Framework
Implementa uma arquitetura estruturada com diferentes modos de operação:
- Route: Direciona para o agente mais apropriado  
- Coordinate: Coordena múltiplos agentes para uma resposta
- Collaborate: Todos os agentes trabalham na mesma tarefa

Baseado na documentação oficial: https://docs.agno.com/teams/introduction
"""

import os
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
# Importar agentes especializados
from .specialists.data_specialist import create_data_specialist
from .specialists.code_specialist import create_code_specialist  
from .specialists.finance_specialist import create_finance_specialist
from .specialists.web_specialist import create_web_specialist
from .specialists.github_specialist import create_github_specialist

from config.settings import get_storage_path

logger = logging.getLogger(__name__)

class AgnoTeamsManager:
    """Gerenciador centralizado dos teams do Agno.
    
    Implementa os três modos do Agno Teams:
    - Route Mode: Direciona para o especialista mais apropriado
    - Coordinate Mode: Coordena múltiplos agentes para resposta sintética
    - Collaborate Mode: Todos os agentes trabalham na mesma tarefa
    
    Recursos avançados:
    - Memória persistente entre sessões
    - Histórico de conversas 
    - Session summaries
    - Configuração flexível de teams
    """
    
    def __init__(self, enable_memory: bool = True, enable_history: bool = True):
        self.teams: Dict[str, Team] = {}
        self.enable_memory = enable_memory
        self.enable_history = enable_history
        
        # Configurar memória persistente se habilitada
        if self.enable_memory:
            self.memory_db = SqliteMemoryDb(
                table_name="teams_memory", 
                db_file=get_storage_path("teams_memory.db")
            )
            self.memory = Memory(db=self.memory_db)
        else:
            self.memory = None
            
        # Configuração padrão para modelos
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente. Configure no arquivo .env")
        
        self.default_model = Gemini(id="gemini-2.0-flash-thinking-exp-01-21", api_key=api_key)
        
    def _get_common_team_config(self, name: str, mode: str, description: str) -> Dict[str, Any]:
        """Retorna configuração comum para todos os teams."""
        config = {
            "name": name,
            "mode": mode,
            "model": self.default_model,
            "description": description,
            "show_members_responses": True,
            "markdown": True,
        }
        
        if self.enable_memory and self.memory:
            config.update({
                "memory": self.memory,
                "enable_agentic_memory": True,
            })
            
        if self.enable_history:
            config.update({
                "add_history_to_messages": True,
                "num_history_runs": 5,
                "enable_session_summaries": True,
            })
            
        return config
        
    def create_main_assistant_team(self) -> Team:
        """Cria o team principal que atua como assistente geral (Route Mode).
        
        Este team analisa a solicitação do usuário e direciona para o 
        especialista mais apropriado. É o ponto de entrada principal.
        """
        
        # Criar agentes especializados
        specialists = [
            create_data_specialist(),
            create_code_specialist(),
            create_finance_specialist(),
            create_web_specialist(),
            create_github_specialist()
        ]
        
        # Configuração do team principal
        config = self._get_common_team_config(
            name="Main Assistant Team",
            mode="route",
            description="Assistente principal que direciona tarefas para especialistas"
        )
        
        # Instruções específicas para o team leader
        instructions = [
            "🎯 Você é o líder de um team de especialistas em diferentes áreas.",
            "",
            "📋 ESPECIALISTAS DISPONÍVEIS:",
            "• Data Specialist: análise de dados, CSV, visualizações, estatísticas",
            "• Code Specialist: análise de código, debugging, programação",  
            "• Finance Specialist: dados financeiros, ações, análise econômica",
            "• Web Specialist: pesquisas na web, informações atuais",
            "• GitHub Specialist: repositórios, código no GitHub, pull requests",
            "",
            "🔍 PROCESSO DE DECISÃO:",
            "1. Analise cuidadosamente a solicitação do usuário",
            "2. Identifique qual especialista é mais apropriado",
            "3. Direcione para esse especialista específico",
            "4. Se a tarefa for ambígua, escolha o especialista mais próximo",
            "",
            "⚡ PALAVRAS-CHAVE PARA DIRECIONAMENTO:",
            "• 'dados', 'CSV', 'análise', 'gráfico' → Data Specialist",
            "• 'código', 'python', 'debug', 'função' → Code Specialist",
            "• 'ação', 'bolsa', 'preço', 'financeiro' → Finance Specialist", 
            "• 'pesquisa', 'notícias', 'web', 'buscar' → Web Specialist",
            "• 'github', 'repositório', 'git', 'commit' → GitHub Specialist",
        ]
        
        main_team = Team(
            members=specialists,
            instructions=instructions,
            **config
        )
        
        self.teams["main"] = main_team
        return main_team
    
    def create_research_team(self) -> Team:
        """Cria um team especializado em pesquisa (Coordinate Mode).
        
        Este team coordena múltiplos especialistas para realizar pesquisas
        abrangentes, combinando diferentes fontes e perspectivas.
        """
        
        # Especialistas para pesquisa
        research_specialists = [
            create_web_specialist(),
            create_data_specialist(), 
            create_github_specialist()
        ]
        
        config = self._get_common_team_config(
            name="Research Team",
            mode="coordinate", 
            description="Team especializado em pesquisa abrangente"
        )
        
        instructions = [
            "🔬 Você coordena uma equipe de pesquisa especializada.",
            "",
            "📊 PROCESSO DE PESQUISA COORDENADA:",
            "1. Web Specialist: busca informações atuais e tendências",
            "2. Data Specialist: analisa dados quantitativos relacionados",
            "3. GitHub Specialist: encontra projetos e código relevante",
            "",
            "🎯 OBJETIVOS:",
            "• Coletar informações de múltiplas fontes",
            "• Analisar dados de diferentes perspectivas", 
            "• Fornecer contexto técnico e prático",
            "• Sintetizar tudo em insights acionáveis",
            "",
            "📝 FORMATO DA RESPOSTA:",
            "• Resumo executivo com principais achados",
            "• Seções específicas por especialista",
            "• Conclusões e recomendações integradas",
            "• Todas as fontes e links relevantes citados",
        ]
        
        research_team = Team(
            members=research_specialists,
            instructions=instructions,
            **config
        )
        
        self.teams["research"] = research_team
        return research_team
    
    def create_development_team(self) -> Team:
        """Cria um team especializado em desenvolvimento (Collaborate Mode).
        
        Este team permite que múltiplos especialistas trabalhem 
        colaborativamente na mesma tarefa, cada um contribuindo 
        com sua expertise única.
        """
        
        # Especialistas para desenvolvimento
        dev_specialists = [
            create_code_specialist(),
            create_github_specialist(),
            create_data_specialist()  # Para análise de logs/métricas
        ]
        
        config = self._get_common_team_config(
            name="Development Team",
            mode="collaborate",
            description="Team colaborativo para desenvolvimento de software"
        )
        
        instructions = [
            "👨‍💻 Vocês são um team de desenvolvimento trabalhando colaborativamente.",
            "",
            "🏗️ CONTRIBUIÇÕES POR ESPECIALISTA:",
            "• Code Specialist: análise técnica, debugging, melhores práticas",
            "• GitHub Specialist: gestão de repositórios, workflows, CI/CD",
            "• Data Specialist: análise de métricas, logs, performance",
            "",
            "🤝 PROCESSO COLABORATIVO:",
            "1. Todos analisam o problema simultaneamente",
            "2. Cada um contribui com sua perspectiva especializada",
            "3. Trabalhem em conjunto para soluções completas",
            "4. Considerem aspectos técnicos, de processo e qualidade",
            "",
            "📋 ASPECTOS A CONSIDERAR:",
            "• Qualidade e legibilidade do código",
            "• Estrutura de projeto e organização",
            "• Performance e escalabilidade",
            "• Testes e documentação",
            "• Workflows de desenvolvimento",
        ]
        
        dev_team = Team(
            members=dev_specialists,
            instructions=instructions,
            **config
        )
        
        self.teams["development"] = dev_team
        return dev_team
    
    def create_analysis_team(self) -> Team:
        """Cria um team especializado em análise de dados (Coordinate Mode).
        
        Este team coordena especialistas em dados, finanças e web para
        fornecer análises abrangentes com múltiplas perspectivas.
        """
        
        # Especialistas para análise
        analysis_specialists = [
            create_data_specialist(),
            create_finance_specialist(),
            create_web_specialist()
        ]
        
        config = self._get_common_team_config(
            name="Analysis Team", 
            mode="coordinate",
            description="Team especializado em análise de dados e insights"
        )
        
        instructions = [
            "📊 Você coordena uma equipe de análise especializada.",
            "",
            "🔄 PROCESSO DE ANÁLISE COORDENADA:",
            "1. Data Specialist: análise técnica e estatística dos dados",
            "2. Finance Specialist: contexto econômico e financeiro",
            "3. Web Specialist: informações externas e contexto de mercado",
            "",
            "🎯 OBJETIVOS DA ANÁLISE:",
            "• Identificar padrões e tendências nos dados",
            "• Fornecer contexto econômico e de mercado",
            "• Correlacionar com informações externas",
            "• Gerar insights acionáveis para tomada de decisão",
            "",
            "📈 FORMATO DA RESPOSTA:",
            "• Resumo executivo com principais insights",
            "• Análise técnica detalhada",
            "• Contexto econômico/financeiro relevante",
            "• Recomendações baseadas em dados sólidos",
            "• Limitações e sugestões para análises futuras",
        ]
        
        analysis_team = Team(
            members=analysis_specialists,
            instructions=instructions,
            **config
        )
        
        self.teams["analysis"] = analysis_team
        return analysis_team
    
    def get_team(self, team_name: str) -> Optional[Team]:
        """Retorna um team específico."""
        return self.teams.get(team_name)
    
    def list_teams(self) -> List[str]:
        """Lista todos os teams disponíveis."""
        return list(self.teams.keys())
    
    def get_team_info(self, team_name: str) -> Optional[Dict[str, Any]]:
        """Retorna informações detalhadas sobre um team."""
        team = self.get_team(team_name)
        if not team:
            return None
            
        return {
            "name": team.name,
            "mode": team.mode,
            "description": team.description,
            "members": [member.name for member in team.members],
            "member_count": len(team.members),
            "has_memory": bool(self.enable_memory),
            "has_history": bool(self.enable_history),
        }
    
    def create_custom_team(self, 
                          name: str,
                          mode: str, 
                          specialists: List[str],
                          description: str = "",
                          custom_instructions: List[str] = None) -> Team:
        """Cria um team customizado com especialistas específicos.
        
        Args:
            name: Nome do team
            mode: "route", "coordinate" ou "collaborate"
            specialists: Lista de especialistas ["data", "code", "finance", "web", "github"]
            description: Descrição do team
            custom_instructions: Instruções específicas (opcional)
        """
        
        # Mapeamento de especialistas
        specialist_map = {
            "data": create_data_specialist,
            "code": create_code_specialist,
            "finance": create_finance_specialist,
            "web": create_web_specialist,
            "github": create_github_specialist
        }
        
        # Validar especialistas
        invalid_specialists = [s for s in specialists if s not in specialist_map]
        if invalid_specialists:
            raise ValueError(f"Especialistas inválidos: {invalid_specialists}")
            
        # Criar instâncias dos especialistas
        team_members = [specialist_map[s]() for s in specialists]
        
        # Configuração do team
        config = self._get_common_team_config(name, mode, description)
        
        # Usar instruções customizadas ou padrão
        if custom_instructions:
            instructions = custom_instructions
        else:
            instructions = [
                f"🎯 Team {name} operando em modo {mode}.",
                f"👥 Especialistas: {', '.join(specialists)}",
                "📋 Trabalhem de acordo com o modo configurado.",
            ]
        
        custom_team = Team(
            members=team_members,
            instructions=instructions,
            **config
        )
        
        # Armazenar o team
        safe_name = name.lower().replace(" ", "_")
        self.teams[safe_name] = custom_team
        
        return custom_team
    
    def initialize_all_teams(self) -> Dict[str, Team]:
        """Inicializa todos os teams padrão disponíveis."""
        teams = {
            "main": self.create_main_assistant_team(),
            "research": self.create_research_team(),
            "development": self.create_development_team(),
            "analysis": self.create_analysis_team(),
        }
        return teams
    
    def get_session_summary(self, team_name: str) -> Optional[str]:
        """Retorna o resumo da sessão para um team específico."""
        team = self.get_team(team_name)
        if team and hasattr(team, 'get_session_summary'):
            summary = team.get_session_summary()
            return summary.summary if summary else None
        return None
    
    def clear_team_history(self, team_name: str) -> bool:
        """Limpa o histórico de um team específico."""
        team = self.get_team(team_name)
        if team and hasattr(team, 'clear_conversation'):
            team.clear_conversation()
            return True
        return False

# Instância global do gerenciador com configuração padrão
teams_manager = AgnoTeamsManager(enable_memory=True, enable_history=True)

# Função utilitária para criar team manager customizado
def create_teams_manager(enable_memory: bool = True, enable_history: bool = True) -> AgnoTeamsManager:
    """Cria uma nova instância do gerenciador de teams com configurações específicas."""
    return AgnoTeamsManager(enable_memory=enable_memory, enable_history=enable_history)

# Constantes para facilitar o uso
TEAM_MODES = {
    "ROUTE": "route",
    "COORDINATE": "coordinate", 
    "COLLABORATE": "collaborate"
}

AVAILABLE_SPECIALISTS = ["data", "code", "finance", "web", "github"]
