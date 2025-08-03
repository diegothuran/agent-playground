from typing import List
import subprocess
import ast
import os

class CodeAnalysisTools:
    """Ferramentas para análise e geração de código."""
    
    def __init__(self):
        self.name = "code_analysis"
    
    def analyze_python_file(self, file_path: str) -> dict:
        """Analisa um arquivo Python e retorna informações sobre sua estrutura."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            tree = ast.parse(content)
            
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
            
            return {
                "file_path": file_path,
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "lines_of_code": len(content.split('\n'))
            }
        except Exception as e:
            return {"error": f"Erro ao analisar arquivo: {str(e)}"}
    
    def check_code_style(self, file_path: str) -> dict:
        """Verifica o estilo do código usando flake8."""
        try:
            result = subprocess.run(
                ['flake8', file_path], 
                capture_output=True, 
                text=True
            )
            return {
                "file_path": file_path,
                "style_issues": result.stdout.split('\n') if result.stdout else [],
                "clean": len(result.stdout.strip()) == 0
            }
        except FileNotFoundError:
            return {"error": "flake8 não está instalado"}
        except Exception as e:
            return {"error": f"Erro ao verificar estilo: {str(e)}"}
    
    def generate_docstring(self, function_code: str) -> str:
        """Gera uma docstring para uma função Python."""
        try:
            tree = ast.parse(function_code)
            func_node = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_node = node
                    break
            
            if not func_node:
                return "Função não encontrada no código fornecido."
            
            args = [arg.arg for arg in func_node.args.args]
            
            docstring = f'"""Descrição da função {func_node.name}.\n\n'
            
            if args:
                docstring += "Args:\n"
                for arg in args:
                    docstring += f"    {arg}: Descrição do parâmetro {arg}.\n"
            
            docstring += "\nReturns:\n    Descrição do retorno.\n"
            docstring += '"""'
            
            return docstring
        except Exception as e:
            return f"Erro ao gerar docstring: {str(e)}"
