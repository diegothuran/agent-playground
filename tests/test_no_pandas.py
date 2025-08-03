#!/usr/bin/env python3
"""
Teste da nova implementação que evita pandas
"""

import csv
import io

def test_no_pandas_approach(file_path):
    """Testa a abordagem sem pandas inicialmente"""
    
    print(f"🧪 Testando abordagem sem pandas para: {file_path}")
    
    try:
        # Ler como bytes
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
        
        # Usar CSV reader do Python
        csv_reader = csv.reader(io.StringIO(text_content))
        
        # Processar dados
        all_rows = list(csv_reader)
        if not all_rows:
            raise ValueError("Arquivo vazio")
        
        header = [col.strip() for col in all_rows[0]]
        data_rows = all_rows[1:]
        
        print(f"📋 Header: {header}")
        print(f"📊 Dados: {len(data_rows)} linhas")
        
        # Limitar dados
        if len(data_rows) > 100:
            data_rows = data_rows[:100]
            print("⚠️ Limitado a 100 linhas para teste")
        
        # Normalizar dados
        cleaned_data = []
        for row in data_rows:
            # Ajustar número de colunas
            while len(row) < len(header):
                row.append('')
            row = row[:len(header)]
            
            # Limpar cada célula
            cleaned_row = []
            for cell in row:
                clean_cell = str(cell).strip() if cell is not None else ''
                cleaned_row.append(clean_cell)
            cleaned_data.append(cleaned_row)
        
        print(f"✅ Dados limpos: {len(cleaned_data)} linhas")
        
        # Criar CSV manualmente
        csv_lines = []
        csv_lines.append(",".join(f'"{col}"' for col in header))
        
        for row in cleaned_data[:50]:  # Apenas 50 linhas
            escaped_row = []
            for cell in row:
                escaped_cell = str(cell).replace('"', '""')
                escaped_row.append(f'"{escaped_cell}"')
            csv_lines.append(",".join(escaped_row))
        
        csv_content = "\n".join(csv_lines)
        print(f"✅ CSV criado manualmente: {len(csv_content)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    file_path = "/home/diego/Downloads/mes01.csv"
    
    print("🧠 Teste da Abordagem Sem Pandas")
    print("=" * 50)
    
    if test_no_pandas_approach(file_path):
        print("\n🎉 ABORDAGEM SEM PANDAS FUNCIONOU!")
        print("✅ O frontend deve funcionar agora!")
    else:
        print("\n❌ Ainda há problemas")

if __name__ == "__main__":
    main()
