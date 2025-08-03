#!/usr/bin/env python3
"""
Teste da nova abordagem com parser CSV puro
"""

import pandas as pd
import csv
import io

def test_pure_csv_parser(file_path):
    """Testa o parser CSV puro"""
    
    print(f"🧪 Testando parser CSV puro para: {file_path}")
    
    try:
        # Ler arquivo como a nova versão do frontend
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Decodificar
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                text_content = content.decode(encoding)
                print(f"✅ Decodificado com {encoding}")
                break
            except UnicodeDecodeError:
                continue
        else:
            text_content = content.decode('utf-8', errors='ignore')
            print("✅ Decodificado com utf-8 (ignorando erros)")
        
        # Usar módulo CSV do Python
        csv_reader = csv.reader(io.StringIO(text_content))
        
        # Ler header
        header = next(csv_reader)
        header = [col.strip() for col in header]
        print(f"📋 Header: {header}")
        
        # Ler dados (limitado)
        data_rows = []
        row_count = 0
        for row in csv_reader:
            if row_count >= 100:  # Testar apenas 100 linhas
                break
            # Ajustar número de colunas
            while len(row) < len(header):
                row.append('')
            row = row[:len(header)]
            data_rows.append(row)
            row_count += 1
        
        print(f"📊 Dados lidos: {len(data_rows)} linhas")
        
        # Agora tentar criar DataFrame
        print("🔄 Criando DataFrame...")
        df = pd.DataFrame(data_rows, columns=header)
        print(f"✅ DataFrame criado: {df.shape}")
        
        # Testar conversão para CSV
        print("🔄 Testando conversão para CSV...")
        csv_output = df.to_csv(index=False)
        print(f"✅ Conversão funcionou: {len(csv_output)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    file_path = "/home/diego/Downloads/mes01.csv"
    
    print("🧠 Teste do Parser CSV Puro")
    print("=" * 50)
    
    if test_pure_csv_parser(file_path):
        print("\n🎉 PARSER CSV PURO FUNCIONOU!")
        print("✅ O frontend deve funcionar agora com a nova abordagem")
    else:
        print("\n❌ Parser CSV puro falhou")
        print("🔧 Problema pode estar ainda mais profundo")

if __name__ == "__main__":
    main()
