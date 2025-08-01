# Makefile para o Agno Playground

SHELL := /bin/bash

.PHONY: help setup install run orchestrated advanced example examples example-orchestrator test clean check-gemini frontend frontend-setup dev-all dev-orchestrated

# Mostra ajuda
help:
	@echo "🎯 Agno Playground - Comandos Disponíveis"
	@echo "========================================"
	@echo ""
	@echo "🔧 CONFIGURAÇÃO"
	@echo "setup           - Configura o ambiente virtual e dependências"
	@echo "install         - Instala dependências básicas"
	@echo "frontend-setup  - Configura o frontend Agent UI"
	@echo "check-gemini    - Verifica configuração do Google Gemini"
	@echo ""
	@echo "🚀 EXECUÇÃO"
	@echo "run             - Inicia o playground principal"
	@echo "orchestrated    - Inicia o playground com orquestrador inteligente (RECOMENDADO)"
	@echo "advanced        - Inicia o playground avançado"
	@echo "frontend        - Inicia o frontend Agent UI"
	@echo "dev-all         - Inicia backend + frontend juntos"
	@echo "dev-orchestrated - Inicia orquestrador + frontend juntos"
	@echo ""
	@echo "📚 EXEMPLOS"
	@echo "examples        - Lista todos os exemplos disponíveis"
	@echo "example         - Executa exemplo básico"
	@echo "example-multi   - Executa exemplo multi-agente"
	@echo "example-tools   - Executa exemplo de ferramentas customizadas"
	@echo "example-data    - Executa exemplo de análise de dados"
	@echo "example-orchestrator - Executa exemplo do orquestrador (NOVO!)"
	@echo "example-mcp     - Executa exemplo de GitHub MCP (NOVO!)"
	@echo "example-data-exploration - Executa exemplo de Exploração Avançada MCP (NOVO!)"
	@echo ""
	@echo "🧪 TESTES"
	@echo "test            - Executa testes básicos"
	@echo "test-quick      - Teste rápido dos agentes"
	@echo "test-charts     - Testa sistema de gráficos automático (NOVO!)"
	@echo "test-data-exploration - Testa MCP de Exploração de Dados (NOVO!)"
	@echo ""
	@echo "🧹 MANUTENÇÃO"
	@echo "clean           - Remove arquivos temporários"
	@echo ""
	@echo "Uso: make <comando>"

# Configuração inicial completa
setup:
	@echo "🚀 Configurando Agno Playground..."
	python3 -m venv .venv
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install -r requirements.txt
	@if [ ! -f .env ]; then cp .env.example .env; fi
	mkdir -p storage logs
	@echo "✅ Configuração concluída!"
	@echo "❗ Configure sua GOOGLE_API_KEY no arquivo .env"
	@echo "💡 Execute 'make check-gemini' para verificar"

# Instala apenas dependências básicas
install:
	@echo "📦 Instalando dependências..."
	./.venv/bin/pip install python-dotenv google-genai requests fastapi uvicorn
	@echo "✅ Dependências básicas instaladas!"

# Executa o playground principal
run:
	@echo "🎮 Iniciando Agno Playground..."
	@if [ ! -f .env ]; then echo "❌ Arquivo .env não encontrado. Execute 'make setup'"; exit 1; fi
	source .venv/bin/activate && python playground.py

# Executa o playground avançado
advanced:
	@echo "🤖 Iniciando Playground Avançado..."
	@if [ ! -f .env ]; then echo "❌ Arquivo .env não encontrado. Execute 'make setup'"; exit 1; fi
	source .venv/bin/activate && python advanced_playground.py

# Executa o playground com orquestrador inteligente
orchestrated:
	@echo "🧠 Iniciando Playground com Orquestrador Inteligente..."
	@if [ ! -f .env ]; then echo "❌ Arquivo .env não encontrado. Execute 'make setup'"; exit 1; fi
	source .venv/bin/activate && python orchestrated_playground.py

# Lista todos os exemplos disponíveis
examples:
	@echo "📚 Exemplos Disponíveis do Agno Playground"
	@echo "=========================================="
	@echo ""
	@echo "example             - Uso básico do playground"
	@echo "example-multi       - Conversas entre múltiplos agentes"
	@echo "example-tools       - Ferramentas customizadas"
	@echo "example-data        - Fluxo de análise de dados"
	@echo "example-charts      - Sistema de gráficos automático (NOVO!)"
	@echo "example-orchestrator - Demonstração do orquestrador (NOVO!)"
	@echo ""
	@echo "💡 Use 'make <exemplo>' para executar"

# Executa exemplo básico
example:
	@echo "📚 Executando exemplo básico..."
	source .venv/bin/activate && python examples/basic_usage.py

# Executa exemplo multi-agente
example-multi:
	@echo "🤖 Executando exemplo multi-agente..."
	source .venv/bin/activate && python examples/multi_agent_conversation.py

# Executa exemplo de ferramentas customizadas
example-tools:
	@echo "🛠️ Executando exemplo de ferramentas customizadas..."
	source .venv/bin/activate && python examples/custom_tools_example.py

# Executa exemplo de análise de dados
example-data:
	@echo "📊 Executando exemplo de análise de dados..."
	source .venv/bin/activate && python examples/data_analysis_workflow.py

# Executa exemplo de gráficos automáticos
example-charts:
	@echo "📈 Executando exemplo de gráficos automáticos..."
	source .venv/bin/activate && python examples/chart_example.py

# Executa exemplo do orquestrador
example-orchestrator:
	@echo "🧠 Executando exemplo do orquestrador..."
	source .venv/bin/activate && python examples/orchestrator_example.py

# Executa testes básicos
test:
	@echo "🧪 Executando testes básicos..."
	source .venv/bin/activate && python tests/test_playground.py

# Teste rápido dos agentes
test-quick:
	@echo "🧪 Executando teste rápido dos agentes..."
	source .venv/bin/activate && python tests/test_quick_agents.py

# Teste de geração de gráficos  
test-charts:
	@echo "� Testando sistema de gráficos automático..."
	source .venv/bin/activate && python examples/chart_example.py

# Teste do MCP de Exploração de Dados
test-data-exploration:
	@echo "� Testando MCP de Exploração de Dados..."
	source .venv/bin/activate && python tests/test_data_exploration_mcp.py

# Remove arquivos temporários
clean:
	@echo "🧹 Limpando arquivos temporários..."
	rm -rf __pycache__/
	rm -rf */__pycache__/
	rm -rf */*/__pycache__/
	rm -rf *.pyc
	rm -rf */*.pyc
	rm -rf */*/*.pyc
	rm -rf .pytest_cache/
	rm -rf storage/*.db
	rm -rf logs/*.log
	@echo "✅ Limpeza concluída!"

# Verifica configuração do Gemini
check-gemini:
	@echo "🤖 Verificando configuração do Google Gemini..."
	source .venv/bin/activate && python scripts/check_gemini.py

# Comando para desenvolvimento
dev: setup
	@echo "🔧 Ambiente de desenvolvimento configurado!"
	@echo "💡 Execute 'make run' para iniciar o playground"

# Configura o frontend Agent UI
frontend-setup:
	@echo "🎨 Configurando Frontend Agent UI..."
	@if [ ! -d "frontend" ]; then \
		echo "📥 Criando frontend..."; \
		npx create-agent-ui@latest frontend; \
	fi
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "📦 Instalando dependências do frontend..."; \
		cd frontend && pnpm install; \
	fi
	@echo "✅ Frontend configurado!"
	@echo "💡 Execute 'make frontend' para iniciar"

# Inicia o frontend Agent UI
frontend:
	@echo "🎨 Iniciando Frontend Agent UI..."
	@if [ ! -d "frontend" ]; then \
		echo "❌ Frontend não encontrado. Execute 'make frontend-setup'"; \
		exit 1; \
	fi
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "❌ Dependências não instaladas. Execute 'make frontend-setup'"; \
		exit 1; \
	fi
	cd frontend && pnpm dev

# Inicia backend + frontend juntos
dev-all:
	@echo "🚀 Iniciando Backend + Frontend..."
	@if [ ! -f .env ]; then echo "❌ Arquivo .env não encontrado. Execute 'make setup'"; exit 1; fi
	@if [ ! -d "frontend/node_modules" ]; then echo "❌ Frontend não configurado. Execute 'make frontend-setup'"; exit 1; fi
	@echo "🎮 Iniciando backend em background..."
	@(source .venv/bin/activate && python playground.py > logs/backend.log 2>&1 &)
	@sleep 3
	@echo "🎨 Iniciando frontend..."
	@echo "📱 Frontend: http://localhost:3000"
	@echo "🔗 Backend: http://localhost:7777"
	cd frontend && pnpm dev

# Inicia orquestrador + frontend juntos (RECOMENDADO)
dev-orchestrated:
	@echo "🧠 Iniciando Orquestrador + Frontend..."
	@if [ ! -f .env ]; then echo "❌ Arquivo .env não encontrado. Execute 'make setup'"; exit 1; fi
	@if [ ! -d "frontend/node_modules" ]; then echo "❌ Frontend não configurado. Execute 'make frontend-setup'"; exit 1; fi
	@echo "🎯 Iniciando orquestrador em background..."
	@(source .venv/bin/activate && python orchestrated_playground.py > logs/orchestrator.log 2>&1 &)
	@sleep 3
	@echo "🎨 Iniciando frontend..."
	@echo "📱 Frontend: http://localhost:3000"
	@echo "🔗 Orquestrador: http://localhost:7777"
	@echo "🧠 Modo: Seleção automática de agentes"
	cd frontend && pnpm dev

# Exemplo de MCP GitHub
example-mcp:
	@echo "🔗 Executando exemplo de GitHub MCP..."
	source .venv/bin/activate && python examples/github_mcp_example.py

# Exemplo de Exploração de Dados MCP
example-data-exploration:
	@echo "🔍 Executando exemplo de Exploração de Dados MCP..."
	source .venv/bin/activate && python examples/data_exploration_mcp_example.py
