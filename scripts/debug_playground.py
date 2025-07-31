#!/usr/bin/env python3
"""Script para verificar os métodos disponíveis no Playground do Agno."""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agno.playground import Playground
    from agents.web_agent import create_web_agent
    
    # Cria um agente de teste
    web_agent = create_web_agent()
    
    # Cria o playground COM agentes
    playground = Playground(agents=[web_agent])
    
    print("🔍 Métodos disponíveis no Playground:")
    methods = [method for method in dir(playground) if not method.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
    
    print(f"\n📋 Tipo do método serve: {type(getattr(playground, 'serve', None))}")
    
    # Verifica a assinatura do método serve
    import inspect
    if hasattr(playground, 'serve'):
        sig = inspect.signature(playground.serve)
        print(f"🔧 Assinatura do método serve: {sig}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
