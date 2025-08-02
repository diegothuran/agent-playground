import pandas as pd
import numpy as np
from typing import Union, List, Dict, Any

class DataAnalysisTools:
    """Ferramentas simplificadas para análise de dados (sem visualizações)."""
    
    def __init__(self):
        self.name = "data_analysis"
    
    def load_csv(self, data: str) -> dict:
        """Carrega dados CSV de uma string e retorna informações básicas."""
        try:
            # Simular carregamento de CSV a partir de string
            import io
            df = pd.read_csv(io.StringIO(data))
            
            result = {
                "success": True,
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "data_types": df.dtypes.to_dict(),
                "sample_data": df.head().to_dict(),
                "basic_stats": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else "Nenhuma coluna numérica",
                "null_counts": df.isnull().sum().to_dict(),
                "info": f"Dataset com {df.shape[0]} linhas e {df.shape[1]} colunas"
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "info": "Erro ao processar dados CSV"
            }
    
    def statistical_summary(self, data: str) -> dict:
        """Calcula estatísticas descritivas dos dados."""
        try:
            import io
            df = pd.read_csv(io.StringIO(data))
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return {
                    "success": False,
                    "error": "Nenhuma coluna numérica encontrada",
                    "info": "Não é possível calcular estatísticas para dados não numéricos"
                }
            
            stats = {}
            for col in numeric_cols:
                stats[col] = {
                    "count": int(df[col].count()),
                    "mean": float(df[col].mean()),
                    "median": float(df[col].median()),
                    "std": float(df[col].std()),
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "q25": float(df[col].quantile(0.25)),
                    "q75": float(df[col].quantile(0.75))
                }
            
            return {
                "success": True,
                "statistics": stats,
                "info": f"Estatísticas calculadas para {len(numeric_cols)} colunas numéricas"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "info": "Erro ao calcular estatísticas"
            }
    
    def correlation_analysis(self, data: str) -> dict:
        """Analisa correlações entre variáveis numéricas."""
        try:
            import io
            df = pd.read_csv(io.StringIO(data))
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) < 2:
                return {
                    "success": False,
                    "error": "Necessário pelo menos 2 colunas numéricas para correlação",
                    "info": "Análise de correlação requer múltiplas variáveis numéricas"
                }
            
            correlation_matrix = df[numeric_cols].corr()
            
            # Encontrar correlações mais fortes
            correlations = []
            for i, col1 in enumerate(numeric_cols):
                for j, col2 in enumerate(numeric_cols):
                    if i < j:  # Evitar duplicatas
                        corr_value = correlation_matrix.loc[col1, col2]
                        correlations.append({
                            "variable1": col1,
                            "variable2": col2,
                            "correlation": float(corr_value),
                            "strength": self._interpret_correlation(corr_value)
                        })
            
            # Ordenar por força da correlação
            correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
            
            return {
                "success": True,
                "correlation_matrix": correlation_matrix.to_dict(),
                "correlations": correlations,
                "info": f"Análise de correlação entre {len(numeric_cols)} variáveis"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "info": "Erro ao calcular correlações"
            }
    
    def create_visualization(self, data: str, chart_type: str = "summary") -> dict:
        """Placeholder para visualizações (desabilitado temporariamente)."""
        return {
            "success": False,
            "error": "Visualizações temporariamente desabilitadas",
            "info": "Use load_csv e statistical_summary para análise de dados",
            "suggestion": "As estatísticas descritivas estão disponíveis via statistical_summary"
        }
    
    def _interpret_correlation(self, corr_value: float) -> str:
        """Interpreta a força da correlação."""
        abs_corr = abs(corr_value)
        if abs_corr >= 0.8:
            return "Muito forte"
        elif abs_corr >= 0.6:
            return "Forte"
        elif abs_corr >= 0.4:
            return "Moderada"
        elif abs_corr >= 0.2:
            return "Fraca"
        else:
            return "Muito fraca"
