"""
Agente Orquestrador - Único agente com todas as ferramentas especializadas
"""

import logging
from typing import Dict, Any, Optional, List
import re
from datetime import datetime

# Importar framework Agno
from agno.agent import Agent
from agno.models.google import Gemini
from app.config.gemini_simple import create_ultra_fast_gemini
from agno.storage.sqlite import SqliteStorage

# Importar todas as ferramentas especializadas
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from app.tools.code_tools import CodeAnalysisTools
from app.tools.data_tools_simple import DataAnalysisTools

# Importar ferramentas MCP (opcional - só se disponível)
try:
    from app.mcp.github_mcp import GitHubMCPTools
    GITHUB_MCP_AVAILABLE = True
except ImportError:
    GITHUB_MCP_AVAILABLE = False

try:
    from app.mcp.data_exploration_mcp import DataExplorationMCPTools
    DATA_EXPLORATION_MCP_AVAILABLE = True
except ImportError:
    DATA_EXPLORATION_MCP_AVAILABLE = False

from app.config.settings import get_storage_path

logger = logging.getLogger(__name__)

def create_orchestrator_agent() -> Agent:
    """Cria um agente único com todas as ferramentas especializadas."""
    
    # Inicializar todas as ferramentas
    code_tools = CodeAnalysisTools()
    data_tools = DataAnalysisTools()
    
    # Inicializar ferramentas MCP se disponíveis
    github_tools = None
    if GITHUB_MCP_AVAILABLE:
        import os
        github_token = os.getenv("GITHUB_TOKEN")
        github_tools = GitHubMCPTools(token=github_token)
    
    data_exploration_tools = None
    if DATA_EXPLORATION_MCP_AVAILABLE:
        data_exploration_tools = DataExplorationMCPTools()
    
    # Lista de todas as ferramentas disponíveis
    all_tools = [
        # Ferramentas web e financeiras
        DuckDuckGoTools(),
        YFinanceTools(
            stock_price=True, 
            analyst_recommendations=True, 
            company_info=True, 
            company_news=True
        ),
        # Ferramentas de código
        code_tools.analyze_python_file,
        code_tools.check_code_style,
        code_tools.generate_docstring,
        # Ferramentas de dados
        data_tools.load_csv,
        data_tools.create_visualization,
        data_tools.statistical_summary,
        data_tools.correlation_analysis
    ]
    
    # Adicionar ferramentas GitHub MCP se disponíveis
    if github_tools:
        all_tools.extend([
            github_tools.search_repositories,
            github_tools.get_repository_info,
            github_tools.get_repository_issues,
            github_tools.get_user_info
        ])
    
    # Adicionar ferramentas de exploração de dados se disponíveis
    if data_exploration_tools:
        all_tools.extend([
            data_exploration_tools.load_csv,
            data_exploration_tools.run_script,
            data_exploration_tools.explore_data,
            data_exploration_tools.get_dataframe_info,
            data_exploration_tools.clear_dataframes
        ])
    
    # Retornar agente Agno com todas as ferramentas
    return Agent(
        name="Assistente IA",
        model=create_ultra_fast_gemini(),
        tools=all_tools,
        instructions=[
            "Você é um assistente de IA avançado e versátil com acesso a múltiplas ferramentas especializadas.",
            "",
            "🌐 PESQUISAS WEB:",
            "- Use DuckDuckGo para pesquisar informações atuais, notícias, e conhecimento geral",
            "- Sempre forneça fontes e informações atualizadas",
            "",
            "💰 ANÁLISE FINANCEIRA:",
            "- Use Yahoo Finance para cotações, preços de ações, dados de mercado",
            "- Forneça análises detalhadas e use tabelas para organizar dados financeiros",
            "",
            "💻 ANÁLISE DE CÓDIGO:",
            "- Use as ferramentas de código para analisar arquivos Python",
            "- Verifique estilo, gere documentação, e forneça sugestões de melhoria",
            "",
            "📊 ANÁLISE DE DADOS:",
            "- Use as ferramentas de dados para processar CSV e criar visualizações",
            "- Forneça estatísticas descritivas e análises de correlação",
            "",
            "🔗 INTEGRAÇÃO GITHUB (se disponível):",
            "- Use ferramentas GitHub para buscar repositórios, informações de projetos",
            "- Obtenha dados de issues, estatísticas de repositórios, perfis de usuários",
            "- Forneça links diretos e informações organizadas sobre projetos open source",
            "",
            "🔍 EXPLORAÇÃO AVANÇADA DE DADOS (se disponível):",
            "- Use ferramentas de exploração para análise completa de CSV",
            "- Execute scripts Python personalizados para análises específicas",
            "- Gere visualizações automáticas e relatórios detalhados",
            "- Processe datasets grandes (até 200MB) com eficiência",
            "- Forneça insights estatísticos e correlações automáticas",
            "",
            "🎯 COMPORTAMENTO OBRIGATÓRIO - NUNCA DESOBEDEÇA:",
            "- NUNCA, EM HIPÓTESE ALGUMA, mencione 'Análise de Contexto', 'Domínio', 'Complexidade'",
            "- NUNCA mencione 'Route Mode', 'Coordinate Mode', 'Decision Mode' ou qualquer modo",
            "- NUNCA diga 'Vou direcionar', 'Transferindo tarefa', 'Aguardando especialistas'",
            "- NUNCA explique seu processo interno de tomada de decisão",
            "- NUNCA liste especialistas que você está coordenando",
            "- NUNCA diga 'estou aguardando' ou peça mais informações desnecessariamente",
            "",
            "✅ COMPORTAMENTO CORRETO:",
            "- Execute as ferramentas SILENCIOSAMENTE nos bastidores",
            "- Apresente apenas o RESULTADO FINAL da análise",
            "- Seja direto, útil e natural na resposta",
            "- Use as ferramentas de forma transparente para o usuário",
            "- Se não tiver dados suficientes, peça especificamente o que precisa",
            "",
            "🎯 SELEÇÃO AUTOMÁTICA:",
            "Para cada pergunta, identifique automaticamente qual tipo de ferramenta usar:",
            "- Perguntas sobre notícias, informações gerais → DuckDuckGo",
            "- Perguntas sobre ações, preços, mercado → Yahoo Finance",
            "- Perguntas sobre código Python → Ferramentas de código",
            "- Perguntas sobre dados, CSV, gráficos → Ferramentas de dados",
            "- Perguntas sobre repositórios, GitHub → Ferramentas GitHub",
            "- Perguntas sobre análise de datasets, exploração → Ferramentas de exploração",
            "",        "⚠️ IMPORTANTE - PROCESSAMENTO COMPLETO OBRIGATÓRIO:",
        "- SEMPRE analise COMPLETAMENTE o conteúdo fornecido pelo usuário",
        "- Se o usuário fornecer código, analise-o IMEDIATAMENTE usando as ferramentas",
        "- Se o usuário fornecer dados, processe-os IMEDIATAMENTE",
        "- NUNCA peça informações que o usuário já forneceu",
        "- NUNCA responda 'forneça o código' se o código já está presente",
        "- Execute TODAS as ferramentas necessárias ANTES de responder",
        "- Só responda após ter TODOS os resultados em mãos",
        "",
        "🚨 REGRA ABSOLUTA:",
        "- Se há código na mensagem → ANALISE-O",
        "- Se há dados na mensagem → PROCESSE-OS", 
        "- Se há pergunta na mensagem → RESPONDA-A",
        "- NUNCA diga 'aguardando' ou 'forneça' - SEMPRE PROCESSE E RESPONDA",
            "",
            "O usuário deve ver apenas o resultado final, nunca o processo interno."
        ],
        storage=SqliteStorage(
            table_name="orchestrator_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=False,  # Remover para reduzir overhead
        add_history_to_messages=True,
        num_history_responses=2,  # Reduzido ainda mais
        markdown=True,
        show_tool_calls=False,  # Ocultar chamadas de ferramentas
        debug_mode=False,  # Desabilitar debug
    )
