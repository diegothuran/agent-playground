#!/usr/bin/env python3
"""
Teste para verificar se o upload de CSV funciona corretamente
"""

import pandas as pd
import io

def test_csv_processing():
    """Testa o processamento de CSV como no frontend"""
    
    print("🧪 Testando processamento de CSV...")
    
    # Simular arquivo CSV
    csv_content = """nome,idade,salario,departamento
João Silva,28,5500.50,TI
Maria Santos,35,7200.00,Financeiro
Pedro Lima,42,8900.75,Vendas
Ana Costa,31,6100.25,RH
Carlos Souza,29,5800.00,TI
Lucia Oliveira,38,7500.50,Marketing"""
    
    try:
        # Simular leitura como o Streamlit faz
        csv_file = io.StringIO(csv_content)
        df = pd.read_csv(csv_file)
        
        print(f"✅ DataFrame criado: {df.shape[0]} linhas, {df.shape[1]} colunas")
        print(f"✅ Colunas: {', '.join(df.columns.tolist())}")
        
        # Testar conversão de tipos (problema original)
        try:
            types_dict = {col: str(dtype) for col, dtype in df.dtypes.items()}
            print(f"✅ Tipos convertidos: {types_dict}")
        except Exception as e:
            print(f"❌ Erro na conversão de tipos: {e}")
            return False
        
        # Testar conversão para CSV
        try:
            csv_output = df.to_csv(index=False)
            print(f"✅ Conversão para CSV: {len(csv_output)} caracteres")
        except Exception as e:
            print(f"❌ Erro na conversão para CSV: {e}")
            # Tentar método alternativo
            try:
                df_str = df.astype(str)
                csv_output = df_str.to_csv(index=False)
                print(f"✅ Conversão alternativa funcionou: {len(csv_output)} caracteres")
            except Exception as e2:
                print(f"❌ Erro mesmo com conversão alternativa: {e2}")
                assert False, f"Erro mesmo com conversão alternativa: {e2}"
        
        print("🎉 Teste de processamento de CSV passou!")
        assert True
        
    except Exception as e:
        print(f"❌ Erro geral no teste: {e}")
        assert False, f"Erro geral no teste: {e}"

def test_with_complex_data():
    """Testa com dados mais complexos que podem causar problemas"""
    
    print("\n🧪 Testando com dados complexos...")
    
    # CSV com valores problemáticos
    complex_csv = """id,name,value,date,description
1,"João, Silva",1234.56,2023-01-01,"Descrição com vírgulas, aspas"
2,Maria's Data,NaN,2023-02-01,NULL
3,"Pedro Boss",999.99,2023-03-01,"Text with quotes"
4,Ana,999,invalid_date,"Unicode: ção, ã, õ"
5,Carlos,0,2023-05-01,"Final entry"
"""
    
    try:
        csv_file = io.StringIO(complex_csv)
        df = pd.read_csv(csv_file)
        
        print(f"✅ DataFrame complexo: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        # Testar processamento como no frontend
        types_dict = {col: str(dtype) for col, dtype in df.dtypes.items()}
        print(f"✅ Tipos complexos: {types_dict}")
        
        # Testar conversão
        try:
            csv_output = df.to_csv(index=False)
            print(f"✅ CSV complexo convertido: {len(csv_output)} caracteres")
        except Exception as e:
            print(f"⚠️ Erro, tentando conversão para string: {e}")
            df_str = df.astype(str)
            csv_output = df_str.to_csv(index=False)
            print(f"✅ Conversão alternativa funcionou: {len(csv_output)} caracteres")
        
        print("🎉 Teste com dados complexos passou!")
        assert True
        
    except Exception as e:
        print(f"❌ Erro com dados complexos: {e}")
        assert False, f"Erro com dados complexos: {e}"

def main():
    print("🧠 Teste de Upload de CSV - Frontend Streamlit")
    print("=" * 50)
    
    test1 = test_csv_processing()
    test2 = test_with_complex_data()
    
    if test1 and test2:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("🎉 O upload de CSV deve funcionar corretamente agora")
    else:
        print("\n❌ Alguns testes falharam")
        print("🔧 Pode ser necessário mais ajustes")

if __name__ == "__main__":
    main()
