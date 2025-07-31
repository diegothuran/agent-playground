# 🎮 Agno Playground

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://typescriptlang.org)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agno](https://img.shields.io/badge/Powered%20by-Agno-green.svg)](https://github.com/phidatahq/agno)

> **Um playground interativo e poderoso para experimentar com agentes de IA especializados usando o framework Agno e Google Gemini.**

## ✨ Características

- 🧠 **Assistente IA Unificado** - Uma única interface que acessa automaticamente múltiplas especialidades
- 🌐 **Pesquisas Web** - Informações atuais via DuckDuckGo
- 💰 **Análise Financeira** - Dados de mercado em tempo real via Yahoo Finance
- 💻 **Análise de Código** - Review, documentação e style check para Python
- 📊 **Análise de Dados** - Processamento de CSV, visualizações e estatísticas
- 🎨 **Interface Moderna** - Frontend em Next.js com TypeScript e Tailwind CSS
- 🔗 **Extensível** - Suporte a Model Context Protocol (MCP) para integrações

## 🚀 Início Rápido

### Pré-requisitos

- **Python 3.9+**
- **Node.js 18+** (para o frontend)
- **Chave API do Google Gemini** ([obter aqui](https://makersuite.google.com/app/apikey))

### Instalação Automática

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/agno-playground.git
cd agno-playground

# 2. Configure o ambiente completo
make setup
make frontend-setup

# 3. Configure sua chave do Google Gemini
cp .env.example .env
# Edite .env e adicione sua GOOGLE_API_KEY

# 4. Inicie o assistente inteligente + frontend
make dev-orchestrated
```

**Pronto!** Acesse:

- **Frontend Moderno**: <http://localhost:3000>
- **Assistente IA**: <http://localhost:7777>

### Assistente IA Inteligente 🧠

O coração do projeto é um **assistente único** que automaticamente seleciona as ferramentas certas para cada pergunta:

```text
💰 "Qual o preço atual da PETR4?"
   → Usa automaticamente Yahoo Finance

🌐 "Quais as últimas notícias sobre IA?"
   → Usa automaticamente DuckDuckGo

💻 "Analise este código Python"
   → Usa automaticamente ferramentas de código

📊 "Como analisar dados de vendas?"
   → Usa automaticamente ferramentas de dados
```

## 📁 Estrutura do Projeto

```text
agno-playground/
├── 🤖 agents/           # Agentes especializados
├── 🛠️ tools/            # Ferramentas customizadas
├── 🔗 mcp/              # Model Context Protocol
├── ⚙️ config/           # Configurações
├── 📚 examples/         # Exemplos de uso
├── 🧪 tests/            # Testes automatizados
├── 📜 scripts/          # Scripts utilitários
├── 📝 logs/             # Logs do sistema
├── 💾 storage/          # Dados dos agentes
├── 🎨 frontend/         # Interface web moderna
├── 🎮 playground.py     # Playground principal
├── 🔬 advanced_playground.py # Playground avançado
└── 📋 requirements.txt  # Dependências
```

## 🤖 Assistente IA Inteligente

### 🧠 Uma IA, Múltiplas Especialidades

- **Experiência Unificada** - Um único assistente que domina várias áreas
- **Seleção Automática** - Escolhe automaticamente a especialidade certa
- **Transparente** - Você não precisa saber sobre agentes especializados
- **Inteligente** - Analisa padrões e contexto para decidir a abordagem

### 🎯 Especialidades Disponíveis (Automáticas)

- 🌐 **Pesquisas Web** - Informações atuais, notícias, conhecimento geral
- 💰 **Análise Financeira** - Cotações, dados de mercado, análise de investimentos
- 💻 **Programação** - Análise de código, documentação, debugging
- 📊 **Análise de Dados** - Processamento de CSV, visualizações, estatísticas
- 🔗 **Integrações** - Conectividade com serviços externos via MCP

**💡 Simplesmente faça sua pergunta - o assistente cuidará do resto!**

### 🎯 Exemplos de Perguntas que Funcionam Automaticamente

```text
💰 "Qual o preço atual da PETR4?"
   → Usa automaticamente Yahoo Finance

🌐 "Quais as últimas notícias sobre inteligência artificial?"
   → Usa automaticamente DuckDuckGo

💻 "Analise este código Python: def hello(): print('world')"
   → Usa automaticamente ferramentas de código

📊 "Como posso analisar dados de vendas em um arquivo CSV?"
   → Usa automaticamente ferramentas de dados

🔍 "Como está o mercado financeiro hoje?"
   → Usa automaticamente pesquisa web + dados financeiros
```

## 📚 Exemplos

Execute os exemplos prontos:

```bash
make examples           # Lista todos os exemplos
make example            # Exemplo básico
make example-multi      # Múltiplos agentes colaborando
make example-tools      # Ferramentas customizadas
make example-data       # Análise de dados
make example-mcp        # Integração MCP
```

## ⚙️ Comandos Disponíveis

### 🔧 Configuração

```bash
make setup              # Configuração completa do ambiente
make install            # Instala apenas dependências básicas
make check-gemini       # Verifica configuração do Gemini
```

### 🚀 Execução

```bash
# 🧠 MODO ORQUESTRADOR (RECOMENDADO)
make orchestrated       # Orquestrador apenas
make dev-orchestrated   # Orquestrador + Frontend

# 🎮 MODO CLÁSSICO
make run                # Playground principal (backend apenas)
make advanced           # Playground avançado (backend apenas)
make dev-all            # Backend + Frontend juntos

# 🎨 FRONTEND APENAS
make frontend           # Frontend Agent UI (interface moderna)
```

## 🎨 Frontend Agent UI

O projeto inclui uma interface web moderna construída com Next.js, Tailwind CSS e TypeScript:

### ✨ Características do Frontend

- 💬 **Interface de Chat Moderna**: Design limpo com suporte a streaming
- 🧩 **Visualização de Tool Calls**: Mostra chamadas de ferramentas e resultados
- 🧠 **Passos de Raciocínio**: Exibe o processo de raciocínio dos agentes
- 📚 **Suporte a Referências**: Mostra fontes utilizadas pelos agentes
- 🖼️ **Multi-modalidade**: Suporta imagens, vídeo e áudio
- 🎨 **Interface Customizável**: Construída com Tailwind CSS

### 🚀 Como Usar o Frontend

```bash
# Configuração inicial (apenas uma vez)
make frontend-setup

# Iniciar apenas o frontend (requer backend rodando)
make frontend

# Iniciar backend + frontend juntos (recomendado)
make dev-all
```

**URLs:**

- Frontend: <http://localhost:3000>
- Backend API: <http://localhost:7777>

### 🧪 Testes

```bash
make test               # Executa todos os testes
make test-quick         # Teste rápido dos agentes
make test-structure     # Valida estrutura do projeto
make test-examples      # Testa os exemplos
```

### 🧹 Manutenção

```bash
make clean              # Remove arquivos temporários
```

## 📋 Pré-requisitos

- **Python 3.9+**
- **pip** (gerenciador de pacotes)
- **Chave API do Google Gemini** ([obter aqui](https://makersuite.google.com/app/apikey))

## 🛠️ Instalação Manual

Se preferir instalar manualmente:

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd agno-playground

# 2. Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua GOOGLE_API_KEY

# 5. Teste a instalação
python playground.py
```

## 🚨 Solução de Problemas

### Erro: ModuleNotFoundError

```bash
# Reinstale as dependências
make clean
make setup
```

### Erro: GOOGLE_API_KEY not found

```bash
# 1. Obtenha sua chave em: https://makersuite.google.com/app/apikey
# 2. Configure no arquivo .env
echo "GOOGLE_API_KEY=sua_chave_aqui" >> .env
# 3. Teste
make check-gemini
```

### Erro: Falha na criação de agentes

```bash
# Teste básico primeiro
make test-quick

# Se falhar, verifique dependências
pip install --upgrade agno google-genai
```

## 🎯 Como Usar

### 1. **Playground Básico**

Execute `make run` e acesse <http://localhost:7777>

- Interface web interativa
- Chat com agentes individuais
- Ferramentas básicas disponíveis

### 2. **Playground Avançado**

Execute `make advanced` para:

- Todos os agentes carregados
- Ferramentas especializadas
- Capacidades de colaboração

### 3. **Desenvolvimento**

- Modifique agentes em `agents/`
- Adicione ferramentas em `tools/`
- Crie exemplos em `examples/`
- Execute testes com `make test`

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Execute os testes: `make test`
4. Faça commit das mudanças
5. Abra um Pull Request

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🔗 Links Úteis

- [Framework Agno](https://github.com/phidatahq/agno)
- [Google Gemini API](https://makersuite.google.com/app/apikey)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)

---

**🎮 Divirta-se explorando o mundo dos agentes de IA!**
