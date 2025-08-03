#!/usr/bin/env python3
"""
Teste específico para o arquivo mes01.csv que está causando erro
"""

import pandas as pd
import numpy as np
import io

def test_problematic_csv():
    """Testa o arquivo específico que está causando problemas"""
    
    print("🧪 Testando arquivo problemático mes01.csv...")
    
    try:
        # Tentar ler o arquivo com diferentes métodos
        file_path = "/home/diego/Downloads/mes01.csv"
        
        print("📂 Tentando ler o arquivo...")
        
        # Método 1: Leitura padrão
        try:
            df = pd.read_csv(file_path)
            print(f"✅ Leitura padrão: {df.shape[0]} linhas, {df.shape[1]} colunas")
        except Exception as e:
            print(f"❌ Erro na leitura padrão: {e}")
            
            # Método 2: Com encoding diferente
            try:
                df = pd.read_csv(file_path, encoding='latin-1')
                print(f"✅ Leitura com latin-1: {df.shape[0]} linhas, {df.shape[1]} colunas")
            except Exception as e2:
                print(f"❌ Erro com latin-1: {e2}")
                return False
        
        # Testar colunas
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Testar tipos individualmente
        print("🔍 Testando tipos de dados...")
        for col in df.columns:
            try:
                dtype = df[col].dtype
                print(f"  - {col}: {dtype} (OK)")
            except Exception as e:
                print(f"  - {col}: ERRO - {e}")
        
        # Testar conversão para string dos tipos
        print("🔧 Testando conversão de tipos...")
        try:
            types_info = []
            for col in df.columns:
                try:
                    dtype_str = str(df[col].dtype)
                    types_info.append(f"{col}: {dtype_str}")
                except Exception as e:
                    print(f"⚠️ Erro no tipo da coluna {col}: {e}")
                    types_info.append(f"{col}: problematic")
            print(f"✅ Tipos convertidos: {types_info}")
        except Exception as e:
            print(f"❌ Erro na conversão de tipos: {e}")
        
        # Testar preview
        print("👀 Testando preview...")
        try:
            preview = df.head(5)
            print(f"✅ Preview funcionou: {preview.shape}")
        except Exception as e:
            print(f"❌ Erro no preview: {e}")
        
        # Testar conversão para CSV - AQUI PODE ESTAR O PROBLEMA
        print("📄 Testando conversão para CSV...")
        try:
            csv_content = df.to_csv(index=False)
            print(f"✅ Conversão CSV funcionou: {len(csv_content)} caracteres")
        except Exception as e:
            print(f"❌ Erro na conversão CSV: {e}")
            
            # Tentar método alternativo
            print("🔧 Tentando método alternativo...")
            try:
                # Converter todas as colunas para string
                df_str = df.astype(str)
                csv_content = df_str.to_csv(index=False)
                print(f"✅ Conversão alternativa funcionou: {len(csv_content)} caracteres")
            except Exception as e2:
                print(f"❌ Erro na conversão alternativa: {e2}")
                
                # Método manual
                print("🛠️ Tentando método manual...")
                try:
                    manual_csv = []
                    header = ",".join([f'"{col}"' for col in df.columns])
                    manual_csv.append(header)
                    
                    for idx, row in df.head(10).iterrows():
                        try:
                            row_values = []
                            for val in row:
                                try:
                                    clean_val = str(val).replace('"', '""')  # Escapar aspas
                                    row_values.append(f'"{clean_val}"')
                                except:
                                    row_values.append('""')
                            manual_csv.append(",".join(row_values))
                        except Exception as row_error:
                            print(f"⚠️ Erro na linha {idx}: {row_error}")
                            continue
                    
                    csv_content = "\n".join(manual_csv)
                    print(f"✅ Método manual funcionou: {len(csv_content)} caracteres")
                    
                except Exception as e3:
                    print(f"❌ Erro no método manual: {e3}")
                    return False
        
        print("🎉 Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def main():
    print("🧠 Teste Específico - Arquivo mes01.csv")
    print("=" * 50)
    
    if test_problematic_csv():
        print("\n✅ ARQUIVO PODE SER PROCESSADO!")
        print("🔧 As correções no frontend devem resolver o problema")
    else:
        print("\n❌ ARQUIVO CONTINUA PROBLEMÁTICO")
        print("💡 Pode ser necessário pré-processamento do arquivo")

if __name__ == "__main__":
    main()
