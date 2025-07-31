"""
Exemplo de fluxo de trabalho para análise de dados no playground Agno.
"""

import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agno.agent import Agent
from agno.models.google import Gemini
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.toolkit import Toolkit
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.log import logger

class DataAnalysisTool(Toolkit):
    """Ferramenta para análise de dados com pandas."""
    
    def __init__(self):
        super().__init__(
            name="Análise de Dados - Realiza análise de dados usando pandas e numpy"
        )
        # Cria dados de exemplo
        self.sample_data = self._create_sample_data()
    
    def _create_sample_data(self) -> pd.DataFrame:
        """Cria um conjunto de dados de exemplo para análise."""
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'date': dates,
            'sales': np.random.normal(1000, 200, 100).round(2),
            'customers': np.random.poisson(50, 100),
            'region': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], 100),
            'product': np.random.choice(['A', 'B', 'C'], 100)
        }
        return pd.DataFrame(data)
    
    def analyze_sales_data(self) -> Dict[str, Any]:
        """
        Analisa os dados de vendas.
        
        Returns:
            Análise estatística dos dados
        """
        try:
            df = self.sample_data
            
            analysis = {
                "total_records": len(df),
                "date_range": {
                    "start": df['date'].min().strftime('%Y-%m-%d'),
                    "end": df['date'].max().strftime('%Y-%m-%d')
                },
                "sales_summary": {
                    "total": df['sales'].sum().round(2),
                    "average": df['sales'].mean().round(2),
                    "median": df['sales'].median().round(2),
                    "std": df['sales'].std().round(2),
                    "min": df['sales'].min().round(2),
                    "max": df['sales'].max().round(2)
                },
                "customers_summary": {
                    "total": df['customers'].sum(),
                    "average": df['customers'].mean().round(2),
                    "median": df['customers'].median(),
                    "min": df['customers'].min(),
                    "max": df['customers'].max()
                },
                "by_region": df.groupby('region')['sales'].agg(['sum', 'mean', 'count']).round(2).to_dict(),
                "by_product": df.groupby('product')['sales'].agg(['sum', 'mean', 'count']).round(2).to_dict(),
                "correlations": df[['sales', 'customers']].corr().round(3).to_dict()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise de dados: {e}")
            return {
                "error": "Erro na análise",
                "message": f"Não foi possível analisar os dados: {str(e)}"
            }
    
    def get_trends(self) -> Dict[str, Any]:
        """
        Identifica tendências nos dados.
        
        Returns:
            Tendências identificadas nos dados
        """
        try:
            df = self.sample_data.copy()
            df['week'] = df['date'].dt.isocalendar().week
            df['month'] = df['date'].dt.month
            
            trends = {
                "weekly_sales": df.groupby('week')['sales'].mean().round(2).to_dict(),
                "monthly_sales": df.groupby('month')['sales'].mean().round(2).to_dict(),
                "daily_pattern": df.groupby(df['date'].dt.dayofweek)['sales'].mean().round(2).to_dict(),
                "growth_rate": {
                    "sales": ((df['sales'].tail(30).mean() / df['sales'].head(30).mean() - 1) * 100).round(2),
                    "customers": ((df['customers'].tail(30).mean() / df['customers'].head(30).mean() - 1) * 100).round(2)
                }
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Erro na análise de tendências: {e}")
            return {
                "error": "Erro na análise de tendências",
                "message": f"Não foi possível identificar tendências: {str(e)}"
            }

def create_data_scientist_agent():
    """Cria um agente especializado em ciência de dados."""
    return Agent(
        name="Data Scientist",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DataAnalysisTool(), DuckDuckGoTools()],
        instructions=[
            "Você é um cientista de dados especializado em análise estatística.",
            "Use as ferramentas de análise para examinar dados de vendas.",
            "Identifique padrões, tendências e insights importantes.",
            "Forneça recomendações baseadas em dados.",
            "Explique suas análises de forma clara e visual quando possível.",
            "Sempre valide suas conclusões com estatísticas apropriadas."
        ],
        storage=SqliteStorage(
            table_name="data_scientist_agent", 
            db_file="storage/data_analysis_example.db"
        ),
        markdown=True,
    )

def create_business_analyst_agent():
    """Cria um agente especializado em análise de negócios."""
    return Agent(
        name="Business Analyst",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é um analista de negócios especializado em interpretar dados.",
            "Transforme insights técnicos em recomendações de negócio.",
            "Foque no impacto comercial e estratégico dos dados.",
            "Sugira ações práticas baseadas nas análises.",
            "Comunique resultados para stakeholders não técnicos."
        ],
        storage=SqliteStorage(
            table_name="business_analyst_agent", 
            db_file="storage/data_analysis_example.db"
        ),
        markdown=True,
    )

def main():
    """Executa o exemplo de análise de dados."""
    print("📊 Exemplo de Análise de Dados do Agno Playground")
    print("=" * 50)
    
    # Cria os agentes especializados
    data_scientist = create_data_scientist_agent()
    business_analyst = create_business_analyst_agent()
    
    # Cria o playground com agentes de análise
    playground = Playground(agents=[data_scientist, business_analyst])
    
    print(f"✅ Playground criado com {len(playground.agents)} agentes:")
    for agent in playground.agents:
        print(f"   • {agent.name}")
    
    print("\n📊 Ferramentas de análise disponíveis:")
    for tool in data_scientist.tools:
        if hasattr(tool, 'name'):
            print(f"   • {tool.name}")
    
    print("\n🌐 Iniciando servidor em http://localhost:7781")
    print("💡 Experimente perguntas como:")
    print("   • 'Analise os dados de vendas disponíveis'")
    print("   • 'Identifique tendências nos dados'")
    print("   • 'Quais recomendações de negócio você sugere?'")
    print("   • 'Compare o desempenho por região'")
    
    # Inicia o servidor
    try:
        app = playground.get_app()
        playground.serve(app, host="localhost", port=7781)
    except KeyboardInterrupt:
        print("\n👋 Exemplo encerrado!")

if __name__ == "__main__":
    main()
