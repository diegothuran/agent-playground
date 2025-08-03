#!/usr/bin/env python3
"""
Script definitivo para aplicar configuração AFC em TODOS os arquivos
"""

import os
import re
from pathlib import Path

def fix_gemini_instances(file_path: Path):
    """Corrige todas as instâncias do Gemini em um arquivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Adicionar import se não existir
        if 'from app.config.gemini_simple import create_ultra_fast_gemini' not in content:
            # Procurar onde adicionar o import
            lines = content.split('\n')
            insert_index = -1
            
            for i, line in enumerate(lines):
                if line.startswith('from agno.models.google import Gemini'):
                    insert_index = i + 1
                    break
                elif line.startswith('from agno.models.google') and 'Gemini' in line:
                    insert_index = i + 1
                    break
            
            if insert_index > 0:
                lines.insert(insert_index, 'from app.config.gemini_simple import create_ultra_fast_gemini')
                content = '\n'.join(lines)
        
        # Substituir todas as instâncias de Gemini(id=...)
        patterns = [
            r'Gemini\(id="[^"]+"\)',
            r'Gemini\(id="[^"]+",\s*api_key=[^)]+\)',
            r'model=Gemini\(id="[^"]+"\)',
            r'model=Gemini\(id="[^"]+",\s*api_key=[^)]+\)',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, 'create_ultra_fast_gemini()', content)
        
        # Se houve mudanças, salvar o arquivo
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Corrigido: {file_path.relative_to(Path.cwd())}")
            return True
        else:
            print(f"⚪ Já correto: {file_path.relative_to(Path.cwd())}")
            return False
            
    except Exception as e:
        print(f"❌ Erro em {file_path}: {e}")
        return False

def main():
    """Corrige todas as instâncias do Gemini no projeto."""
    print("🚀 Aplicando configuração AFC em TODOS os arquivos...")
    
    project_root = Path(__file__).parent.parent.parent
    
    # Arquivos a serem corrigidos
    files_to_fix = [
        "app/backend/agno_teams_playground.py",
        "app/agents/teams_manager.py",
        "app/agents/code_agent.py",
        "app/agents/github_agent.py", 
        "app/agents/web_agent.py",
        "app/agents/mcp_agent.py",
        "app/agents/data_agent.py",
        "app/agents/finance_agent.py",
        "app/agents/data_exploration_agent.py",
        "app/agents/orchestrator_agent.py",
    ]
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        full_path = project_root / file_path
        if full_path.exists():
            if fix_gemini_instances(full_path):
                fixed_count += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {file_path}")
    
    # Limpar cache Python
    print("\n🧹 Limpando cache Python...")
    os.system("find . -name '*.pyc' -delete 2>/dev/null || true")
    os.system("find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true")
    
    print(f"\n🎯 Resumo:")
    print(f"- Arquivos corrigidos: {fixed_count}")
    print(f"- Configuração AFC: max_remote_calls = 3")
    print(f"- Modelo: gemini-2.0-flash-lite")
    print(f"- Temperature: 0.3")
    
    print(f"\n🔄 Para aplicar:")
    print(f"1. Pare o processo atual (Ctrl+C)")
    print(f"2. Execute: make backend") 
    print(f"3. Aguarde logs com: 'AFC is enabled with max remote calls: 3'")
    
    print(f"\n⚡ Agora TODOS os modelos usam a configuração otimizada!")

if __name__ == "__main__":
    main()
