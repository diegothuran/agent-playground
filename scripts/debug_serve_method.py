#!/usr/bin/env python3
"""Investigar o método serve do Agno Playground."""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 Investigando método serve() do Agno Playground")
print("=" * 50)

try:
    from agno.playground import Playground
    from agents.web_agent import create_web_agent
    
    # Criar um agente simples para teste
    agent = create_web_agent()
    playground = Playground(agents=[agent])
    
    print("✅ Playground criado")
    
    # Investigar métodos disponíveis
    print("\n📋 Métodos disponíveis no playground:")
    methods = [method for method in dir(playground) if not method.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
    
    # Investigar especificamente o método serve
    if hasattr(playground, 'serve'):
        import inspect
        serve_signature = inspect.signature(playground.serve)
        print(f"\n🔍 Assinatura do método serve:")
        print(f"  serve{serve_signature}")
        
        # Ver documentação se disponível
        if playground.serve.__doc__:
            print(f"\n📚 Documentação do serve:")
            print(f"  {playground.serve.__doc__}")
    
    # Verificar se existe get_app
    if hasattr(playground, 'get_app'):
        print(f"\n✅ Método get_app existe")
        try:
            app = playground.get_app()
            print(f"  App type: {type(app)}")
        except Exception as e:
            print(f"  ❌ Erro ao chamar get_app(): {e}")
    
    # Verificar se existe run
    if hasattr(playground, 'run'):
        import inspect
        run_signature = inspect.signature(playground.run)
        print(f"\n🏃 Método run encontrado:")
        print(f"  run{run_signature}")
    
    # Verificar se existe start
    if hasattr(playground, 'start'):
        import inspect
        start_signature = inspect.signature(playground.start)
        print(f"\n🚀 Método start encontrado:")
        print(f"  start{start_signature}")
        
    print("\n🎯 Investigação concluída!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
