import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sem display para funcionar em servidores
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
            # Garantir que o backend está configurado
            plt.switch_backend('Agg')
            
            # Criar figura
            plt.figure(figsize=(10, 6))
            
            if isinstance(data, dict):
                x = list(data.keys())
                y = list(data.values())
            elif isinstance(data, list):
                x = range(len(data))
                y = data
            else:
                plt.close()
                return "❌ Formato de dados não suportado. Use list ou dict."
            
            # Verificar se há dados
            if not y:
                plt.close()
                return "❌ Não há dados para visualizar."
            
            # Criar gráfico baseado no tipo
            if chart_type == "line":
                plt.plot(x, y, marker='o', linewidth=2, markersize=4)
            elif chart_type == "bar":
                plt.bar(x, y, alpha=0.7)
            elif chart_type == "scatter":
                plt.scatter(x, y, alpha=0.7, s=50)
            elif chart_type == "histogram":
                plt.hist(y, bins=20, alpha=0.7, edgecolor='black')
            else:
                plt.plot(x, y)  # Fallback para line
            
            # Configurar aparência
            plt.title(f"Gráfico {chart_type.title()}", fontsize=14, fontweight='bold')
            plt.xlabel("X", fontsize=12)
            plt.ylabel("Y", fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            plt.close()  # Garantir que fecha a figura
            error_msg = f"❌ Erro ao criar visualização: {str(e)}"
            print(f"DEBUG: {error_msg}")  # Para debug
            return error_msg
    
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
    
    def create_advanced_visualization(self, df: pd.DataFrame, x_col: str, y_col: str = None, 
                                    chart_type: str = "line", title: str = None) -> str:
        """Cria visualizações avançadas com pandas/seaborn."""
        try:
            # Garantir backend
            plt.switch_backend('Agg')
            
            # Configurar estilo
            sns.set_style("whitegrid")
            plt.figure(figsize=(12, 8))
            
            if chart_type == "correlation":
                # Matriz de correlação (ignora x_col e y_col para este tipo)
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) < 2:
                    plt.close()
                    return "❌ Dados insuficientes para matriz de correlação (precisa de 2+ colunas numéricas)"
                
                corr_matrix = df[numeric_cols].corr()
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                           square=True, linewidths=0.5)
                plt.title(title or "Matriz de Correlação", fontsize=14, fontweight='bold')
                
            elif chart_type == "distribution":
                # Distribuição de uma variável
                if not x_col or x_col not in df.columns:
                    plt.close()
                    return f"❌ Coluna '{x_col}' não encontrada ou não especificada"
                
                if df[x_col].dtype in ['object', 'category']:
                    # Variável categórica
                    df[x_col].value_counts().plot(kind='bar', alpha=0.7)
                    plt.xticks(rotation=45)
                else:
                    # Variável numérica
                    sns.histplot(df[x_col], kde=True, alpha=0.7)
                
                plt.title(title or f"Distribuição de {x_col}", fontsize=14, fontweight='bold')
                plt.xlabel(x_col, fontsize=12)
                plt.ylabel("Frequência", fontsize=12)
                
            elif chart_type == "scatter" and y_col:
                # Gráfico de dispersão
                if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                    plt.close()
                    return f"❌ Colunas não encontradas: {x_col}, {y_col}"
                
                sns.scatterplot(data=df, x=x_col, y=y_col, alpha=0.7)
                plt.title(title or f"{y_col} vs {x_col}", fontsize=14, fontweight='bold')
                
            elif chart_type == "line" and y_col:
                # Gráfico de linha
                if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                    plt.close()
                    return f"❌ Colunas não encontradas: {x_col}, {y_col}"
                
                plt.plot(df[x_col], df[y_col], marker='o', linewidth=2, markersize=4)
                plt.title(title or f"{y_col} ao longo de {x_col}", fontsize=14, fontweight='bold')
                plt.xlabel(x_col, fontsize=12)
                plt.ylabel(y_col, fontsize=12)
                
            elif chart_type == "box":
                # Box plot
                if not x_col or x_col not in df.columns:
                    plt.close()
                    return f"❌ Coluna '{x_col}' não encontrada ou não especificada"
                
                if y_col and y_col in df.columns:
                    sns.boxplot(data=df, x=y_col, y=x_col)
                    plt.title(title or f"Box Plot: {x_col} por {y_col}", fontsize=14, fontweight='bold')
                else:
                    sns.boxplot(y=df[x_col])
                    plt.title(title or f"Box Plot: {x_col}", fontsize=14, fontweight='bold')
            
            else:
                return f"❌ Tipo de gráfico '{chart_type}' não suportado ou parâmetros incorretos"
            
            plt.tight_layout()
            
            # Salvar como data URL
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            plt.close()
            error_msg = f"❌ Erro ao criar visualização avançada: {str(e)}"
            print(f"DEBUG: {error_msg}")
            return error_msg
