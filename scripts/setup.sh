#!/bin/bash

echo "🚀 Configurando Agno Playground..."

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Cria arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo de configuração..."
    cp .env.example .env
    echo "❗ IMPORTANTE: Configure sua OPENAI_API_KEY no arquivo .env"
fi

# Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p storage
mkdir -p logs

echo "✅ Configuração concluída!"
echo ""
echo "📝 Próximos passos:"
echo "1. Configure sua OPENAI_API_KEY no arquivo .env"
echo "2. Execute: python playground.py"
echo "3. Acesse: http://localhost:7777"
