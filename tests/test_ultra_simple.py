#!/usr/bin/env python3
"""
Teste ultra-simples para upload de CSV
"""

def test_simple_upload():
    """Testa abordagem super simples"""
    
    print("🧪 Teste Ultra-Simples - Sem Pandas")
    print("=" * 40)
    
    try:
        # Simular upload do arquivo mes01.csv
        with open('/home/diego/Downloads/mes01.csv', 'rb') as f:
            file_bytes = f.read()
        
        print("✅ Arquivo lido como bytes")
        
        # Tentar decodificar
        file_text = None
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                file_text = file_bytes.decode(encoding)
                print(f"✅ Decodificado com {encoding}")
                break
            except UnicodeDecodeError:
                print(f"❌ Falhou com {encoding}")
                continue
        
        if file_text is None:
            print("❌ Não conseguiu decodificar")
            return False
        
        # Contar linhas
        lines = file_text.strip().split('\n')
        print(f"✅ {len(lines)} linhas encontradas")
        
        # Mostrar primeiras linhas
        print("\n📝 Primeiras linhas:")
        for i, line in enumerate(lines[:5]):
            print(f"L{i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
        
        print(f"\n✅ Tamanho do arquivo: {len(file_text)} caracteres")
        
        # Simular salvamento
        if len(file_text) > 30000:
            sample_lines = lines[:100]
            file_text = '\n'.join(sample_lines)
            print("⚠️ Arquivo limitado a 100 linhas")
        
        print("✅ Arquivo processado com sucesso!")
        print("🎉 MÉTODO ULTRA-SIMPLES FUNCIONOU!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_simple_upload()
