import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List, Dict, Any
import io
import base64

class DataAnalysisTools:
    """Ferramentas para análise de dados e visualização."""
    
    def __init__(self):
        self.name = "data_analysis"
    
    def load_csv(self, file_path: str) -> dict:
        """Carrega um arquivo CSV e retorna informações básicas."""
        try:
            df = pd.read_csv(file_path)
            return {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "head": df.head().to_dict(),
                "description": df.describe().to_dict()
            }
        except Exception as e:
            return {"error": f"Erro ao carregar CSV: {str(e)}"}
    
    def create_visualization(self, data: Union[List, Dict], chart_type: str = "line") -> str:
        """Cria uma visualização dos dados e retorna como base64."""
        try:
            plt.figure(figsize=(10, 6))
            
            if isinstance(data, dict):
                x = list(data.keys())
                y = list(data.values())
            elif isinstance(data, list):
                x = range(len(data))
                y = data
            else:
                return "Formato de dados não suportado"
            
            if chart_type == "line":
                plt.plot(x, y)
            elif chart_type == "bar":
                plt.bar(x, y)
            elif chart_type == "scatter":
                plt.scatter(x, y)
            elif chart_type == "histogram":
                plt.hist(y, bins=20)
            
            plt.title(f"Gráfico {chart_type.title()}")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.grid(True, alpha=0.3)
            
            # Salva o gráfico em base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return image_base64
        except Exception as e:
            return f"Erro ao criar visualização: {str(e)}"
    
    def statistical_summary(self, data: List[float]) -> dict:
        """Calcula resumo estatístico dos dados."""
        try:
            arr = np.array(data)
            return {
                "count": len(arr),
                "mean": float(np.mean(arr)),
                "median": float(np.median(arr)),
                "std": float(np.std(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "q25": float(np.percentile(arr, 25)),
                "q75": float(np.percentile(arr, 75))
            }
        except Exception as e:
            return {"error": f"Erro no cálculo estatístico: {str(e)}"}
    
    def correlation_analysis(self, data: Dict[str, List[float]]) -> dict:
        """Analisa correlações entre variáveis."""
        try:
            df = pd.DataFrame(data)
            correlation_matrix = df.corr()
            return {
                "correlation_matrix": correlation_matrix.to_dict(),
                "strong_correlations": self._find_strong_correlations(correlation_matrix)
            }
        except Exception as e:
            return {"error": f"Erro na análise de correlação: {str(e)}"}
    
    def _find_strong_correlations(self, corr_matrix: pd.DataFrame, threshold: float = 0.7) -> List[dict]:
        """Encontra correlações fortes entre variáveis."""
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_corr.append({
                        "var1": corr_matrix.columns[i],
                        "var2": corr_matrix.columns[j],
                        "correlation": float(corr_value)
                    })
        return strong_corr
