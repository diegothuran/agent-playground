#!/usr/bin/env python3
"""Script para corrigir os caminhos dos imports nos testes movidos."""

import os
import glob

def fix_import_paths():
    """Corrige os caminhos de import nos arquivos de teste."""
    
    # Padrão antigo e novo
    old_path = "sys.path.append(os.path.dirname(os.path.abspath(__file__)))"
    new_path = "sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))"
    
    # Encontrar todos os arquivos Python na pasta de testes
    test_files = glob.glob("/home/diego/Documentos/RA/play/tests/integration/*.py")
    
    for file_path in test_files:
        print(f"🔧 Corrigindo {file_path}...")
        
        try:
            # Ler o arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Substituir o caminho
            if old_path in content:
                content = content.replace(old_path, new_path)
                
                # Escrever de volta
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Corrigido: {os.path.basename(file_path)}")
            else:
                print(f"  ⚠️  Não encontrado padrão em: {os.path.basename(file_path)}")
                
        except Exception as e:
            print(f"  ❌ Erro em {file_path}: {e}")

if __name__ == "__main__":
    print("🔧 Corrigindo caminhos de import nos testes...")
    fix_import_paths()
    print("✅ Correção concluída!")
