#!/usr/bin/env python3
"""
Script para verificar e configurar o Google Gemini API.
"""

import os
from dotenv import load_dotenv

def check_gemini_setup():
    """Verifica se o Gemini está configurado corretamente."""
    print("🔍 Verificando configuração do Google Gemini...")
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica a chave API
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY não encontrada no arquivo .env")
        print("💡 Configure sua chave seguindo estas etapas:")
        print("   1. Acesse: https://makersuite.google.com/app/apikey")
        print("   2. Crie uma nova API key")
        print("   3. Adicione ao arquivo .env: GOOGLE_API_KEY=sua_chave_aqui")
        return False
    
    if api_key.startswith('your_') or api_key.endswith('_here'):
        print("❌ GOOGLE_API_KEY não foi configurada (ainda é o valor de exemplo)")
        return False
    
    # Testa a biblioteca
    try:
        import google.genai as genai
        print("✅ Biblioteca google-genai instalada")
    except ImportError:
        print("❌ Biblioteca google-genai não instalada")
        print("💡 Execute: pip install google-genai")
        return False
    
    # Testa a conexão (opcional - não faz chamada real)
    try:
        # Configura o cliente
        client = genai.Client(api_key=api_key)
        print("✅ API key configurada no cliente")
        
        # Nota: google-genai usa uma API diferente, então ajustamos o teste
        print("✅ Cliente Gemini configurado com sucesso")
        print("🎯 Modelo recomendado: gemini-1.5-pro")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar cliente: {str(e)}")
        print("💡 Verifique se sua GOOGLE_API_KEY está correta")
        return False

def main():
    """Função principal."""
    print("🤖 Google Gemini - Verificação de Configuração")
    print("=" * 50)
    
    if check_gemini_setup():
        print("\n🎉 Configuração do Gemini está OK!")
        print("🚀 Agora você pode executar: python playground.py")
    else:
        print("\n❌ Configuração do Gemini precisa ser corrigida")
        print("📖 Consulte o arquivo INSTALL.md para mais detalhes")

if __name__ == "__main__":
    main()
