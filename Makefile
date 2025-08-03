# 🧠 Agno Teams - Sistema de Agentes Especializados
# Makefile organizado para nova estrutura

.PHONY: help setup backend frontend streamlit full clean test

# Configuração padrão
PYTHON := python3

help: ## Mostra esta mensagem de ajuda
	@echo "🧠 Agno Teams - Sistema de Agentes Especializados"
	@echo "=================================================="
	@echo ""
	@echo "📋 Comandos disponíveis:"
	@echo ""
	@echo "  make setup     - Configuração inicial"
	@echo "  make backend   - Backend apenas (porta 7777)"
	@echo "  make frontend  - Frontend Streamlit (porta 8501)"
	@echo "  make streamlit - Alias para frontend"
	@echo "  make full      - Sistema completo"
	@echo "  make test      - Executar testes"
	@echo "  make clean     - Limpeza do projeto"
	@echo ""
	@echo "🚀 Ou use diretamente:"
	@echo "  python main.py --mode [backend|frontend|full]"

setup: ## Configura o ambiente de desenvolvimento
	@echo "🔧 Configurando ambiente..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "✅ Ambiente configurado!"

backend: ## Executa apenas o backend (Teams API na porta 7777)
	@echo "🚀 Iniciando Agno Teams Backend..."
	$(PYTHON) app/backend/agno_teams_playground.py

frontend: ## Executa apenas o frontend Streamlit (porta 8501)
	@echo "🎨 Iniciando Agno Teams Frontend..."
	$(PYTHON) app/scripts/run_streamlit_frontend.py

streamlit: frontend ## Alias para frontend

full: ## Sistema completo: backend + frontend Streamlit
	@echo "🚀 Iniciando Sistema Completo..."
	$(PYTHON) app/scripts/run_full_streamlit.py

test: ## Executa testes do projeto
	@echo "🧪 Executando testes..."
	$(PYTHON) -m pytest tests/ -v

clean: ## Remove arquivos temporários e cache
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/
	@echo "✅ Limpeza concluída!"