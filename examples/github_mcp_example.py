#!/usr/bin/env python3
"""
Exemplo de uso do MCP GitHub integrado ao Agno Playground

Este exemplo demonstra como usar o assistente orquestrador para interagir
com a API do GitHub através do sistema MCP.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from agents.orchestrator_agent import create_orchestrator_agent


def main():
    """Exemplo principal de uso do GitHub MCP."""
    
    print("🔗 Exemplo: GitHub MCP no Agno Playground")
    print("=" * 50)
    
    # Verificar se o token do GitHub está configurado
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("⚠️  GITHUB_TOKEN não configurado.")
        print("   Para usar a API do GitHub, configure:")
        print("   export GITHUB_TOKEN=seu_token_aqui")
        print("   ou adicione ao arquivo .env")
        print()
    
    # Criar o assistente orquestrador
    print("🤖 Criando assistente orquestrador...")
    assistant = create_orchestrator_agent()
    
    # Exemplos de perguntas que usarão o GitHub MCP automaticamente
    examples = [
        "Busque repositórios Python populares sobre machine learning",
        "Me mostre informações sobre o repositório facebook/react",
        "Quais são as issues abertas no repositório microsoft/vscode?",
        "Me dê informações sobre o usuário GitHub 'torvalds'",
        "Encontre repositórios JavaScript para desenvolvimento de APIs"
    ]
    
    print("\n📋 Exemplos de perguntas que usam GitHub MCP:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n" + "=" * 50)
    print("💡 Dica: O assistente escolherá automaticamente as ferramentas GitHub")
    print("    quando detectar perguntas sobre repositórios, código, ou desenvolvedores.")
    
    # Modo interativo
    print("\n🎯 Modo Interativo (digite 'quit' para sair):")
    while True:
        try:
            question = input("\n❓ Sua pergunta: ").strip()
            
            if question.lower() in ['quit', 'exit', 'sair']:
                print("👋 Até logo!")
                break
            
            if not question:
                continue
            
            print("\n🤖 Assistente:")
            print("-" * 30)
            
            # O assistente irá automaticamente escolher se usar GitHub MCP
            # baseado no conteúdo da pergunta
            response = assistant.run(question)
            print(response.content)
            
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")


if __name__ == "__main__":
    main()
