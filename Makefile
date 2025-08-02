# Agno Teams - Makefile Simplificado
# Apenas 3 formas de execução: backend, frontend, ou sistema completo

.PHONY: help setup backend frontend full clean

# Configuração padrão
PYTHON := python3
VENV_DIR := .venv

help: ## Mostra esta mensagem de ajuda
	@echo "🧠 Agno Teams - Sistema de Agentes Especializados"
	@echo "=================================================="
	@echo ""
	@echo "📋 Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🚀 Formas de execução:"
	@echo "  make backend   - Apenas API backend (porta 7777)"
	@echo "  make frontend  - Apenas interface web (porta 3000)"
	@echo "  make full      - Sistema completo (ambas as portas)"

setup: ## Configura o ambiente de desenvolvimento
	@echo "🔧 Configurando ambiente..."
	$(PYTHON) -m venv $(VENV_DIR)
	./$(VENV_DIR)/bin/pip install --upgrade pip
	./$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "✅ Ambiente configurado!"
	@echo "💡 Ative o ambiente: source $(VENV_DIR)/bin/activate"

backend: ## Executa apenas o backend (Teams API na porta 7777)
	@echo "🚀 Iniciando Agno Teams Backend..."
	$(PYTHON) run_backend.py

frontend: ## Executa apenas o frontend (Interface web na porta 3000)
	@echo "🎨 Iniciando Agno Teams Frontend..."
	$(PYTHON) run_frontend.py

full: ## Executa o sistema completo (backend + frontend)
	@echo "🚀 Iniciando sistema completo..."
	$(PYTHON) run_full.py

clean: ## Remove arquivos temporários e cache
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/
	@echo "✅ Limpeza concluída!"