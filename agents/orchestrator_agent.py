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
from agno.storage.sqlite import SqliteStorage

# Importar todas as ferramentas especializadas
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from tools.code_tools import CodeAnalysisTools
from tools.data_tools import DataAnalysisTools

from config.settings import get_storage_path

logger = logging.getLogger(__name__)

def create_orchestrator_agent() -> Agent:
    """Cria um agente único com todas as ferramentas especializadas."""
    
    # Inicializar todas as ferramentas
    code_tools = CodeAnalysisTools()
    data_tools = DataAnalysisTools()
    
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
    
    # Retornar agente Agno com todas as ferramentas
    return Agent(
        name="Assistente IA",
        model=Gemini(id="gemini-1.5-pro"),
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
            "🎯 SELEÇÃO AUTOMÁTICA:",
            "Para cada pergunta, identifique automaticamente qual tipo de ferramenta usar:",
            "- Perguntas sobre notícias, informações gerais → DuckDuckGo",
            "- Perguntas sobre ações, preços, mercado → Yahoo Finance",
            "- Perguntas sobre código Python → Ferramentas de código",
            "- Perguntas sobre dados, CSV, gráficos → Ferramentas de dados",
            "- Para outras perguntas → Use seu conhecimento base",
            "",
            "Sempre use as ferramentas de forma natural e transparente.",
            "Não mencione qual ferramenta específica você está usando.",
            "Forneça respostas precisas, úteis e bem fundamentadas."
        ],
        storage=SqliteStorage(
            table_name="orchestrator_agent", 
            db_file=get_storage_path("agents.db")
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )
