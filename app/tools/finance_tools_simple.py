"""
Finance Tools - Ferramentas simplificadas para análise financeira
"""

class SimpleFinanceTools:
    """Ferramentas simplificadas para análise financeira."""
    
    def __init__(self):
        self.name = "finance_tools"
    
    def get_stock_price(self, symbol: str) -> dict:
        """Placeholder para obter preço de ações."""
        return {
            "success": False,
            "error": "Funcionalidade de preços em tempo real temporariamente indisponível",
            "info": f"Para obter dados de {symbol}, use fontes externas como Yahoo Finance",
            "suggestion": "Posso ajudar com análise de dados financeiros que você fornecer"
        }
    
    def get_financial_data(self, symbol: str) -> dict:
        """Placeholder para dados financeiros."""
        return {
            "success": False,
            "error": "Dados financeiros em tempo real temporariamente indisponíveis",
            "info": f"Para análise de {symbol}, forneça os dados diretamente",
            "suggestion": "Posso analisar dados financeiros em formato CSV ou texto"
        }
