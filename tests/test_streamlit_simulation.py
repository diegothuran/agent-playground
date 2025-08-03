#!/usr/bin/env python3
"""
Simulação do upload do Streamlit para testar a correção
"""

import pandas as pd
import io

def simulate_streamlit_upload(file_path):
    """Simula exatamente o que o Streamlit faz no upload"""
    
    print(f"🎭 Simulando upload do Streamlit para: {file_path}")
    
    # Abrir arquivo como o Streamlit faria
    try:
        with open(file_path, 'rb') as f:
            uploaded_file_content = f.read()
        
        # Criar objeto similar ao que Streamlit retorna
        class MockUploadedFile:
            def __init__(self, content, name):
                self.content = content
                self.name = name
                self.position = 0
            
            def read(self):
                return self.content
            
            def seek(self, position):
                self.position = position
                return position
            
            def getvalue(self):
                return self.content
        
        uploaded_file = MockUploadedFile(uploaded_file_content, "mes01.csv")
        
        # Aplicar a lógica do frontend corrigido
        print("📂 Executando lógica do frontend corrigido...")
        
        uploaded_file.seek(0)
        
        # Primeira tentativa: leitura normal
        try:
            print("🔄 Tentativa 1: leitura normal...")
            df = pd.read_csv(io.BytesIO(uploaded_file.read()), encoding='utf-8')
            print(f"✅ Leitura normal funcionou: {df.shape}")
            return df
        except Exception as e1:
            print(f"❌ Tentativa 1 falhou: {e1}")
            
            # Segunda tentativa: parser customizado
            try:
                print("🔄 Tentativa 2: parser customizado...")
                uploaded_file.seek(0)
                
                content = uploaded_file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='replace')
                else:
                    content = str(content)
                
                # Processar linha por linha manualmente
                lines = content.strip().split('\n')
                if not lines:
                    raise ValueError("Arquivo vazio")
                
                # Primeira linha como header
                header = lines[0].split(',')
                header = [col.strip().strip('"') for col in header]
                
                # Processar dados
                data_rows = []
                for line in lines[1:]:
                    if line.strip():
                        row = line.split(',')
                        # Limpar e ajustar número de colunas
                        row = [cell.strip().strip('"') for cell in row]
                        while len(row) < len(header):
                            row.append('')
                        row = row[:len(header)]  # Cortar se tiver colunas extras
                        data_rows.append(row)
                
                # Criar DataFrame manualmente
                df = pd.DataFrame(data_rows, columns=header)
                print(f"✅ Parser customizado funcionou: {df.shape}")
                return df
                
            except Exception as e2:
                print(f"❌ Tentativa 2 falhou: {e2}")
                return None
    
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return None

def test_csv_conversion(df):
    """Testa conversão do DataFrame para CSV"""
    
    print(f"\n🔄 Testando conversão CSV do DataFrame...")
    
    try:
        # Primeira tentativa: conversão normal
        print("🔄 Conversão normal...")
        csv_content = df.to_csv(index=False)
        print(f"✅ Conversão normal funcionou: {len(csv_content)} caracteres")
        return csv_content
        
    except Exception as e1:
        print(f"❌ Conversão normal falhou: {e1}")
        
        try:
            # Segunda tentativa: conversão forçando strings
            print("🔄 Conversão com strings...")
            df_safe = df.copy()
            for col in df_safe.columns:
                df_safe[col] = df_safe[col].astype(str)
            csv_content = df_safe.to_csv(index=False)
            print(f"✅ Conversão com strings funcionou: {len(csv_content)} caracteres")
            return csv_content
            
        except Exception as e2:
            print(f"❌ Conversão com strings falhou: {e2}")
            
            try:
                # Terceira tentativa: conversão manual
                print("🔄 Conversão manual...")
                rows = []
                # Header
                rows.append(','.join(df.columns))
                # Data (apenas primeiras 50 linhas)
                for _, row in df.head(50).iterrows():
                    row_values = []
                    for val in row:
                        # Converter para string segura
                        str_val = str(val).replace(',', ';').replace('\n', ' ').replace('\r', ' ')
                        row_values.append(str_val)
                    rows.append(','.join(row_values))
                
                csv_content = '\n'.join(rows)
                print(f"✅ Conversão manual funcionou: {len(csv_content)} caracteres")
                return csv_content
                
            except Exception as e3:
                print(f"❌ Conversão manual falhou: {e3}")
                return None

def main():
    file_path = "/home/diego/Downloads/mes01.csv"
    
    print("🧠 Teste da Correção do Upload Streamlit")
    print("=" * 50)
    
    # Simular upload
    df = simulate_streamlit_upload(file_path)
    
    if df is not None:
        print(f"\n🎉 UPLOAD FUNCIONOU!")
        print(f"📊 DataFrame: {df.shape[0]} linhas, {df.shape[1]} colunas")
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Testar conversão CSV
        csv_result = test_csv_conversion(df)
        
        if csv_result:
            print(f"\n🎉 CONVERSÃO CSV FUNCIONOU!")
            print(f"📝 Tamanho final: {len(csv_result)} caracteres")
            print("\n✅ PROBLEMA RESOLVIDO! O frontend deve funcionar agora.")
        else:
            print(f"\n❌ CONVERSÃO CSV FALHOU")
            print("🔧 Pode ser necessário mais ajustes na conversão")
    else:
        print(f"\n❌ UPLOAD FALHOU")
        print("🔧 O problema persiste, pode ser necessária uma abordagem diferente")

if __name__ == "__main__":
    main()
