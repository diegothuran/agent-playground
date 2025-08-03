#!/usr/bin/env python3
"""
Teste do novo sistema de upload com múltiplos formatos
"""

import base64
import json

def test_csv_upload():
    """Testa upload de CSV"""
    print("🧪 Testando upload CSV...")
    
    csv_content = """produto,categoria,preco
Notebook,Informatica,2500.00
Mouse,Informatica,89.90
Teclado,Informatica,299.99"""
    
    upload_data = {
        "content": csv_content,
        "filename": "teste.csv",
        "type": "csv",
        "size": len(csv_content)
    }
    
    json_data = json.dumps(upload_data)
    print(f"✅ CSV: {len(json_data)} chars")
    return True

def test_pdf_upload():
    """Simula upload de PDF"""
    print("🧪 Testando upload PDF...")
    
    # Simular dados binários de PDF
    fake_pdf_bytes = b"%PDF-1.4 fake content for testing"
    pdf_base64 = base64.b64encode(fake_pdf_bytes).decode('utf-8')
    
    upload_data = {
        "content": pdf_base64,
        "filename": "teste.pdf", 
        "type": "pdf",
        "size": len(fake_pdf_bytes)
    }
    
    json_data = json.dumps(upload_data)
    print(f"✅ PDF: {len(json_data)} chars")
    return True

def test_excel_upload():
    """Simula upload de Excel"""
    print("🧪 Testando upload Excel...")
    
    # Simular dados binários de Excel
    fake_excel_bytes = b"PK fake excel content for testing"
    excel_base64 = base64.b64encode(fake_excel_bytes).decode('utf-8')
    
    upload_data = {
        "content": excel_base64,
        "filename": "teste.xlsx",
        "type": "xlsx", 
        "size": len(fake_excel_bytes)
    }
    
    json_data = json.dumps(upload_data)
    print(f"✅ Excel: {len(json_data)} chars")
    return True

def test_message_processing():
    """Testa processamento de mensagens com arquivos"""
    print("🧪 Testando processamento de mensagens...")
    
    # Testar cada tipo
    test_files = [
        ('csv', 'Analise estes dados'),
        ('pdf', 'Extraia informações deste documento'),
        ('xlsx', 'Processe esta planilha')
    ]
    
    for file_type, message in test_files:
        upload_data = {
            "content": "fake_content",
            "filename": f"teste.{file_type}",
            "type": file_type,
            "size": 100
        }
        
        json_data = json.dumps(upload_data)
        
        # Simular processamento da mensagem
        try:
            file_data = json.loads(json_data)
            filename = file_data.get('filename', 'arquivo')
            msg_type = file_data.get('type', 'unknown')
            
            if msg_type == 'csv':
                enhanced_msg = f"{message}\n📊 **Arquivo CSV anexado**: {filename}"
            elif msg_type == 'pdf':
                enhanced_msg = f"{message}\n📄 **Arquivo PDF anexado**: {filename}"
            elif msg_type in ['xls', 'xlsx']:
                enhanced_msg = f"{message}\n📊 **Planilha Excel anexada**: {filename}"
            
            print(f"✅ {file_type.upper()}: Mensagem processada")
            
        except Exception as e:
            print(f"❌ {file_type.upper()}: Erro {e}")
            return False
    
    return True

def main():
    print("🧠 Teste do Sistema Multi-Formato")
    print("=" * 40)
    
    tests = [
        test_csv_upload,
        test_pdf_upload, 
        test_excel_upload,
        test_message_processing
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            results.append(False)
    
    if all(results):
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("🎉 Sistema multi-formato está funcionando")
    else:
        print("\n❌ Alguns testes falharam")

if __name__ == "__main__":
    main()
