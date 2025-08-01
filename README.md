# 🎮 Agno Playground

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://typescriptlang.org)
[![Ne### 📚 Exemplos Práticos

```bash
make examples           # Lista todos os exemplos disponíveis
make example            # Exemplo básico de uso
make example-multi      # Múltiplos agentes colaborando  
make example-tools      # Ferramentas customizadas
make example-data       # Análise de dados com gráficos
make example-charts     # Sistema de gráficos automático (NOVO!)
make example-mcp        # Integração MCP (GitHub)
make example-data-exploration # Exploração avançada MCP oficial
```s://img.shields.io/badge/Next.js-15+-black.svg)](https://nextjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agno](https://img.shields.io/badge/Powered%20by-Agno-green.svg)](https://github.com/phidatahq/agno)

> **Playground interativo e profissional para experimentar com agentes de IA especializados, integração de MCPs e análise avançada de dados usando Google Gemini.**

## ✨ Características Principais

- 🧠 **Orquestrador Inteligente** - Agente único que seleciona automaticamente as ferramentas certas para cada tarefa
- 🌐 **Pesquisas Web Avançadas** - Informações atuais e notícias via DuckDuckGo
- 💰 **Análise Financeira Completa** - Dados de mercado, cotações e análises via Yahoo Finance
- 💻 **Análise de Código Profissional** - Review automático, documentação e verificação de estilo Python
- 📊 **Visualização de Dados** - Geração automática de gráficos (line, bar, scatter, histogram, correlation, heatmap)
- 🔍 **Exploração Avançada de Dados** - Processamento de datasets grandes (até 200MB) com MCP oficial
- 🎨 **Interface Web Moderna** - Frontend responsivo em Next.js 15 + TypeScript + Tailwind CSS
- 🔗 **Integrações MCP** - Suporte nativo ao Model Context Protocol para extensibilidade
- 🔄 **Streaming Real-time** - Respostas em tempo real com visualização de tool calls
- 💾 **Persistência Completa** - Histórico de sessões e conversas salvas automaticamente

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │  Chat UI    │ │  Tool Viz   │ │    Session Manager     ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│               Backend (Agno + FastAPI)                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Orquestrador Inteligente                  ││
│  │  ┌───────────┐ ┌───────────┐ ┌─────────────────────────┐││
│  │  │ Selector  │ │ Router    │ │    Context Manager     │││
│  │  └───────────┘ └───────────┘ └─────────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │  Web Tools  │ │ Data Tools  │ │       MCP Tools        ││
│  │ DuckDuckGo  │ │ Matplotlib  │ │  GitHub | DataExplore  ││
│  │ YFinance    │ │ Pandas/CSV  │ │  Custom | Extensions   ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Início Rápido

### Pré-requisitos

- **Python 3.9+** com pip
- **Node.js 18+** com npm/pnpm (para o frontend)
- **Chave API do Google Gemini** ([obter aqui](https://makersuite.google.com/app/apikey))

### Instalação Automática (Recomendada)

```bash
# 1. Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd agno-playground

# 2. Configure o ambiente completo (backend + frontend)
make setup

# 3. Configure sua chave do Google Gemini
cp .env.example .env
# Edite .env e adicione: GOOGLE_API_KEY=sua_chave_aqui

# 4. Inicie o sistema completo
make dev-orchestrated
```

**✅ Sistema iniciado!** Acesse:

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

🔍 "Explore o dataset vendas.csv focando em sazonalidade"
   → Usa automaticamente exploração avançada de dados
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
- 🔍 **Exploração Avançada** - Análise automatizada de datasets, scripts Python customizados
- 🔗 **Integrações** - Conectividade com serviços externos via MCP

### 📊 Sistema de Gráficos Automático (NOVO!)

O playground agora possui **detecção automática de gráficos**! Qualquer ferramenta que gere visualizações será automaticamente exibida no frontend.

**Como usar:**
```text
"Crie um gráfico de barras com vendas: Jan=100, Fev=150, Mar=200"
"Analise o arquivo dados.csv e gere visualizações"
"Mostre uma matriz de correlação dos dados"
```

**Tipos suportados:** Line, Bar, Scatter, Histogram, Heatmap, Box Plot  
**Tecnologia:** Matplotlib → Base64 → Detecção automática no frontend

**💡 Simplesmente faça sua pergunta - o assistente cuidará do resto!**

### 🎯 Exemplos de Perguntas que Funcionam Automaticamente

```text
💰 "Qual o preço atual da PETR4?"
   → Usa automaticamente Yahoo Finance

🌐 "Quais as últimas notícias sobre inteligência artificial?"
   → Usa automaticamente DuckDuckGo

## 🎯 Exemplos de Uso Automático

O sistema detecta automaticamente o tipo de pergunta e seleciona as ferramentas adequadas:

```text
💰 "Qual o preço atual da PETR4?"
   → Usa automaticamente Yahoo Finance

🌐 "Quais as últimas notícias sobre IA?"
   → Usa automaticamente DuckDuckGo

💻 "Analise este código Python: def hello(): print('world')"
   → Usa automaticamente ferramentas de código

📊 "Analise o arquivo vendas.csv e gere insights"
   → Usa automaticamente análise de dados + visualização

📈 "Crie um gráfico de barras com os números [10, 20, 30, 40]"
   → Usa automaticamente ferramentas de gráficos + exibição no frontend

🔍 "Explore o dataset customers.csv focando em churn"
   → Usa automaticamente exploração avançada de dados (MCP)

📊 "Crie um gráfico de barras com as vendas mensais"
   → Usa automaticamente ferramentas de visualização + exibição automática
```

### 📊 Sistema de Gráficos Inteligente (NOVO!)

O playground possui **detecção automática de gráficos**! Qualquer análise que gere visualizações será automaticamente exibida no frontend.

```text
🎯 Como usar:
"Analise vendas.csv e crie gráficos de tendência"
"Mostre um histograma da distribuição de idades"  
"Gere uma matriz de correlação dos dados"

🔧 Tipos suportados:
📈 Line, 📊 Bar, 🔍 Scatter, 📋 Histogram, 🔥 Heatmap, 📦 Box Plot

⚡ Tecnologia:
Backend (Matplotlib) → Base64 → Frontend (Detecção automática)
```

## 📚 Documentação e Exemplos

### 🎮 Exemplos Interativos

```bash
make examples           # Lista todos os exemplos disponíveis
make example            # Exemplo básico de uso
make example-multi      # Múltiplos agentes colaborando  
make example-tools      # Ferramentas customizadas
make example-data       # Análise de dados com gráficos
make example-mcp        # Integração MCP (GitHub)
make example-data-exploration # Exploração avançada MCP oficial
```

### 📖 Documentação Técnica

- **[Guia de MCPs](docs/MCP_GUIDE.md)** - Como usar e criar MCPs
- **[Documentação Confluence](docs/CONFLUENCE_DOCUMENTATION.md)** - Documentação técnica completa
- **[Contribuição](CONTRIBUTING.md)** - Como contribuir com o projeto

## ⚙️ Comandos Make Disponíveis

### 🔧 Setup e Configuração

```bash
make setup              # Configuração completa (backend + frontend)
make install            # Instala apenas dependências Python
make check-gemini       # Verifica configuração do Gemini API
make clean              # Remove arquivos temporários
```

### 🚀 Execução (Escolha seu modo)

```bash
# 🧠 MODO ORQUESTRADOR (RECOMENDADO)
make orchestrated       # Backend orquestrador apenas
make dev-orchestrated   # Backend + Frontend juntos

# 🎮 MODO CLÁSSICO  
make run                # Playground principal
make advanced           # Playground com todos os agentes
make dev-all            # Todos os agentes + Frontend

# 🎨 FRONTEND
make frontend           # Frontend Agent UI apenas
```

### 🧪 Testes e Validação

```bash
make test               # Testes básicos do sistema
make test-quick         # Teste rápido dos agentes
make test-charts        # Valida sistema de gráficos automático (NOVO!)
make test-data-exploration # Testa integração MCP oficial de dados
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

## 🚀 Como Usar o Sistema

### 1. **Modo Recomendado - Orquestrador Inteligente**

```bash
make dev-orchestrated
```

**Acesse**: http://localhost:3000

- ✅ **Interface moderna** com Next.js + Tailwind
- ✅ **Chat streaming** em tempo real
- ✅ **Seleção automática** de ferramentas
- ✅ **Visualização de tool calls** 
- ✅ **Histórico de sessões**

### 2. **Modo Desenvolvimento**

```bash
# Backend apenas
make orchestrated    # http://localhost:7777

# Frontend apenas (requer backend rodando)
make frontend       # http://localhost:3000

# Todos os agentes (modo clássico)
make advanced       # http://localhost:7777
```

### 3. **Extensão e Customização**

- 🧠 **Agentes**: Modifique em `agents/`
- 🛠️ **Ferramentas**: Adicione em `tools/`
- 🔗 **MCPs**: Configure em `mcp/config.json`
- 📚 **Exemplos**: Crie em `examples/`
- 🧪 **Testes**: Adicione em `tests/`

## 🏗️ Arquitetura Técnica

```
┌─────────────────────────────────────────────┐
│            Frontend (Next.js 15)           │
│  🎨 UI + 💬 Chat + 📊 Visualizations      │
└────────────────┬────────────────────────────┘
                 │ HTTP/WebSocket
┌────────────────▼────────────────────────────┐
│         Backend (Agno + FastAPI)           │
│  ┌─────────────────────────────────────────┐│
│  │      🧠 Orquestrador Inteligente       ││
│  └─────────────────────────────────────────┘│
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ Web │ │Data │ │Code │ │MCP  │ │More │  │
│  │Tools│ │Viz  │ │Anal │ │Ext  │ │...  │  │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │
└─────────────────────────────────────────────┘
```

## 📊 Funcionalidades Principais

| Categoria | Ferramentas | Exemplos de Uso |
|-----------|-------------|-----------------|
| **🌐 Web** | DuckDuckGo | "Últimas notícias sobre IA" |
| **💰 Finance** | Yahoo Finance | "Preço atual da PETR4" |
| **💻 Code** | Python Analysis | "Analise este código Python" |
| **📊 Data** | Matplotlib/Pandas | "Crie gráfico dos dados [1,2,3]" |
| **🔍 Advanced** | MCP Data Exploration | "Explore dataset vendas.csv" |
| **🔗 External** | GitHub API | "Busque projetos Python ML" |
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
