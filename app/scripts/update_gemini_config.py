#!/usr/bin/env python3
"""
Script para atualizar todos os specialists com configurações otimizadas do Gemini
"""

import os
import re
from pathlib import Path

def update_specialist_imports(file_path: Path):
    """Atualiza imports em um arquivo specialist."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar import da configuração otimizada se não existir
    if 'from app.config.gemini_config import create_optimized_gemini' not in content:
        # Procurar onde adicionar o import
        lines = content.split('\n')
        insert_index = -1
        
        for i, line in enumerate(lines):
            if line.startswith('from app.config.settings'):
                insert_index = i + 1
                break
        
        if insert_index > 0:
            lines.insert(insert_index, 'from app.config.gemini_config import create_optimized_gemini')
            content = '\n'.join(lines)
    
    # Substituir Gemini(id="...") por create_optimized_gemini()
    content = re.sub(
        r'model=Gemini\(id="[^"]+"\)',
        'model=create_optimized_gemini()',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Atualizado: {file_path.name}")

def main():
    """Atualiza todos os specialists com configurações otimizadas."""
    print("🔧 Atualizando specialists com configurações otimizadas do Gemini...")
    
    # Diretório dos specialists
    specialists_dir = Path(__file__).parent.parent / "agents" / "specialists"
    
    # Arquivos a serem atualizados
    specialist_files = [
        "data_specialist.py",
        "code_specialist.py", 
        "finance_specialist.py",
        "web_specialist.py",
        "github_specialist.py"
    ]
    
    for filename in specialist_files:
        file_path = specialists_dir / filename
        if file_path.exists():
            update_specialist_imports(file_path)
        else:
            print(f"⚠️  Arquivo não encontrado: {filename}")
    
    print("\n🎯 Configurações aplicadas:")
    print("- max_remote_calls: 10 → 3 (melhor latência)")
    print("- temperature: padrão → 0.3 (respostas mais diretas)")
    print("- timeout: padrão → 25s (balanceado)")
    print("- model: gemini-2.0-flash-lite (otimizado)")
    
    print("\n📝 Para aplicar as mudanças:")
    print("1. Reinicie o sistema: Ctrl+C e rode 'make full' novamente")
    print("2. Ou use variáveis de ambiente no .env para ajustar:")
    print("   GEMINI_MAX_REMOTE_CALLS=2  # Para latência ainda menor")
    print("   GEMINI_TEMPERATURE=0.1     # Para respostas mais determinísticas")

if __name__ == "__main__":
    main()
