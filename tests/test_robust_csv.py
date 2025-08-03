#!/usr/bin/env python3
"""
Teste específico para o arquivo mes01.csv problemático
"""

import pandas as pd
import numpy as np
import io

def test_robust_csv_reading(file_path):
    """Testa leitura robusta do CSV problemático"""
    
    print(f"🧪 Testando leitura robusta de: {file_path}")
    
    try:
        # Método 1: Leitura padrão
        print("📂 Método 1: Leitura padrão...")
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"✅ Método 1 funcionou: {df.shape}")
        return df
    except Exception as e1:
        print(f"❌ Método 1 falhou: {e1}")
        
        try:
            # Método 2: Leitura como bytes
            print("📂 Método 2: Leitura como bytes...")
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Decodificar
            try:
                text_content = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text_content = content.decode('latin-1')
                except UnicodeDecodeError:
                    text_content = content.decode('cp1252', errors='ignore')
            
            df = pd.read_csv(io.StringIO(text_content))
            print(f"✅ Método 2 funcionou: {df.shape}")
            return df
            
        except Exception as e2:
            print(f"❌ Método 2 falhou: {e2}")
            
            try:
                # Método 3: Engine python
                print("📂 Método 3: Engine python...")
                df = pd.read_csv(file_path, engine='python', encoding='utf-8', on_bad_lines='skip')
                print(f"✅ Método 3 funcionou: {df.shape}")
                return df
                
            except Exception as e3:
                print(f"❌ Método 3 falhou: {e3}")
                
                try:
                    # Método 4: Leitura linha por linha
                    print("📂 Método 4: Linha por linha...")
                    lines = []
                    with open(file_path, 'rb') as f:
                        for line in f:
                            try:
                                line_str = line.decode('utf-8', errors='ignore').strip()
                                lines.append(line_str)
                            except:
                                continue
                    
                    clean_csv = '\n'.join(lines)
                    df = pd.read_csv(io.StringIO(clean_csv))
                    print(f"✅ Método 4 funcionou: {df.shape}")
                    return df
                    
                except Exception as e4:
                    print(f"❌ Método 4 falhou: {e4}")
                    return None

def analyze_file_content(file_path):
    """Analisa o conteúdo do arquivo para entender o problema"""
    
    print(f"\n🔍 Analisando conteúdo de: {file_path}")
    
    try:
        # Ler primeiros bytes
        with open(file_path, 'rb') as f:
            first_bytes = f.read(100)
        
        print(f"📋 Primeiros 100 bytes: {first_bytes}")
        
        # Tentar diferentes encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                decoded = first_bytes.decode(encoding)
                print(f"✅ {encoding}: {repr(decoded[:50])}")
            except:
                print(f"❌ {encoding}: não conseguiu decodificar")
        
        # Verificar tamanho do arquivo
        import os
        size = os.path.getsize(file_path)
        print(f"📏 Tamanho do arquivo: {size} bytes")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")

def main():
    file_path = "/home/diego/Downloads/mes01.csv"
    
    print("🧠 Diagnóstico do Arquivo CSV Problemático")
    print("=" * 50)
    
    # Analisar conteúdo
    analyze_file_content(file_path)
    
    # Testar leitura robusta
    df = test_robust_csv_reading(file_path)
    
    if df is not None:
        print(f"\n🎉 SUCESSO! Arquivo lido com {df.shape[0]} linhas e {df.shape[1]} colunas")
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Testar conversão para CSV (onde pode estar o problema real)
        try:
            csv_output = df.to_csv(index=False)
            print(f"✅ Conversão para CSV funcionou: {len(csv_output)} caracteres")
        except Exception as e:
            print(f"❌ Erro na conversão para CSV: {e}")
            try:
                df_str = df.astype(str)
                csv_output = df_str.to_csv(index=False)
                print(f"✅ Conversão alternativa funcionou: {len(csv_output)} caracteres")
            except Exception as e2:
                print(f"❌ Conversão alternativa também falhou: {e2}")
        
    else:
        print("\n❌ Todos os métodos falharam")
        print("💡 O arquivo pode estar corrompido ou ter formato muito especial")

if __name__ == "__main__":
    main()
