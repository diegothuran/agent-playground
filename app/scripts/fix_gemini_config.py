#!/usr/bin/env python3
"""
Script para corrigir configurações dos specialists - versão simples e funcional
"""

import os
import re
from pathlib import Path

def fix_specialist_config(file_path: Path):
    """Corrige configuração em um arquivo specialist."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir import problemático
    content = content.replace(
        'from app.config.gemini_config import create_optimized_gemini',
        'from app.config.gemini_simple import create_fast_gemini'
    )
    
    # Substituir chamada da função
    content = content.replace(
        'model=create_optimized_gemini()',
        'model=create_fast_gemini()'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Corrigido: {file_path.name}")

def main():
    """Corrige todos os specialists com configurações funcionais."""
    print("🔧 Corrigindo specialists com configurações simples...")
    
    # Diretório dos specialists
    specialists_dir = Path(__file__).parent.parent / "agents" / "specialists"
    
    # Arquivos a serem corrigidos
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
            fix_specialist_config(file_path)
        else:
            print(f"⚠️  Arquivo não encontrado: {filename}")
    
    print("\n🎯 Configurações aplicadas:")
    print("- Modelo: gemini-2.0-flash-lite (mais rápido)")
    print("- Temperature: 0.3 (respostas diretas)")
    print("- Max tokens: 2048 (balanceado)")
    print("- AFC otimizado via variáveis de ambiente")
    
    print("\n📝 Para aplicar:")
    print("1. As variáveis de ambiente já estão configuradas no .env")
    print("2. Execute: make backend")
    print("3. Aguarde ver: 'AFC is enabled with max remote calls: 3'")

if __name__ == "__main__":
    main()
