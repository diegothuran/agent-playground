"""
Exemplo de como criar e usar ferramentas customizadas no playground Agno.
"""

import os
import sys
import requests
from typing import Dict, Any
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
from agno.utils.log import logger

class WeatherTool(Toolkit):
    """Ferramenta customizada para consultar o clima."""
    
    def __init__(self):
        super().__init__(
            name="Ferramenta de Clima - Consulta informações meteorológicas"
        )
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Obtém informações do clima para uma cidade.
        
        Args:
            city: Nome da cidade para consultar o clima
            
        Returns:
            Dicionário com informações meteorológicas
        """
        try:
            # API gratuita do OpenWeatherMap (requer chave API)
            api_key = os.getenv("OPENWEATHER_API_KEY")
            if not api_key:
                return {
                    "error": "Chave API do OpenWeatherMap não configurada",
                    "message": "Configure OPENWEATHER_API_KEY no arquivo .env"
                }
            
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric",
                "lang": "pt_br"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }
            
        except requests.RequestException as e:
            logger.error(f"Erro ao consultar API do clima: {e}")
            return {
                "error": "Erro de conexão",
                "message": f"Não foi possível consultar o clima para {city}"
            }
        except Exception as e:
            logger.error(f"Erro inesperado na consulta do clima: {e}")
            return {
                "error": "Erro interno",
                "message": "Erro inesperado ao consultar o clima"
            }

class CalculatorTool(Toolkit):
    """Ferramenta customizada para cálculos matemáticos."""
    
    def __init__(self):
        super().__init__(
            name="Calculadora - Realiza cálculos matemáticos básicos e avançados"
        )
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Calcula uma expressão matemática.
        
        Args:
            expression: Expressão matemática para calcular
            
        Returns:
            Resultado do cálculo
        """
        try:
            # Sanitiza a expressão para segurança
            allowed_chars = "0123456789+-*/()., "
            sanitized = "".join(c for c in expression if c in allowed_chars)
            
            if not sanitized:
                return {
                    "error": "Expressão inválida",
                    "message": "A expressão contém caracteres não permitidos"
                }
            
            # Calcula usando eval (cuidado: apenas para expressões simples)
            result = eval(sanitized)
            
            return {
                "expression": expression,
                "result": result,
                "formatted_result": f"{expression} = {result}"
            }
            
        except ZeroDivisionError:
            return {
                "error": "Divisão por zero",
                "message": "Não é possível dividir por zero"
            }
        except Exception as e:
            logger.error(f"Erro no cálculo: {e}")
            return {
                "error": "Erro de cálculo",
                "message": f"Não foi possível calcular: {expression}"
            }

def create_custom_tools_agent():
    """Cria um agente com ferramentas customizadas."""
    return Agent(
        name="Custom Tools Assistant",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[WeatherTool(), CalculatorTool()],
        instructions=[
            "Você é um assistente com ferramentas especializadas.",
            "Use a ferramenta de clima para consultas meteorológicas.",
            "Use a calculadora para operações matemáticas.",
            "Sempre explique o que cada ferramenta faz antes de usá-la.",
            "Seja útil e preciso nas suas respostas."
        ],
        storage=SqliteStorage(
            table_name="custom_tools_agent", 
            db_file="storage/custom_tools_example.db"
        ),
        markdown=True,
    )

def main():
    """Executa o exemplo de ferramentas customizadas."""
    print("🛠️  Exemplo de Ferramentas Customizadas do Agno Playground")
    print("=" * 55)
    
    # Cria um agente com ferramentas customizadas
    agent = create_custom_tools_agent()
    
    # Cria o playground
    playground = Playground(agents=[agent])
    
    print(f"✅ Playground criado com o agente: {agent.name}")
    print("🛠️  Ferramentas disponíveis:")
    for tool in agent.tools:
        print(f"   • {tool.name}: {tool.description}")
    
    print("\n🌐 Iniciando servidor em http://localhost:7779")
    print("💡 Experimente perguntas como:")
    print("   • 'Qual o clima em São Paulo?'")
    print("   • 'Calcule 2 + 2 * 3'")
    print("   • 'Quanto é a raiz quadrada de 144?'")
    
    # Inicia o servidor
    try:
        app = playground.get_app()
        playground.serve(app, host="localhost", port=7779)
    except KeyboardInterrupt:
        print("\n👋 Exemplo encerrado!")

if __name__ == "__main__":
    main()
