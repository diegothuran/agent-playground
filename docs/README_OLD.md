# 🧠 Agno Teams - Sistema de Agentes Especializados

Sistema moderno de agentes especializados usando o framework Agno, com arquitetura de Teams inteligente que analisa contexto e orquestra especialistas automaticamente.

## 🎯 **3 FORMAS DE EXECUÇÃO**

### 1. 🔗 **Backend Apenas** (API REST)
```bash
python run_backend.py
# ou
make backend
```
**Porta**: 7777 | **Uso**: Integração, desenvolvimento backend

### 2. 🎨 **Frontend Apenas** (Interface Web)
```bash
python run_frontend.py  
# ou
make frontend
```
**Porta**: 3000 | **Pré-requisito**: Backend rodando

### 3. 🚀 **Sistema Completo** (Produção)
```bash
python run_full.py
# ou  
make full
```
**Gerencia**: Backend + Frontend simultaneamente

---

## 🏗️ **ARQUITETURA INTELIGENTE**

```
🧠 Team Leader (Análise de Contexto)
├── 💰 Finance Agent (Mercados & Análise Econômica)
├── 🌐 Web Research Agent (Pesquisas & Informações Atuais)  
├── 💻 Code Analysis Agent (Desenvolvimento & Debugging)
├── 📊 Data Analysis Agent (Estatísticas & Visualizações)
└── 🐙 GitHub Agent (Repositórios & Gestão de Código)
```

### **Fluxo Inteligente**
1. **🔍 Análise Semântica**: Team Leader analisa contexto da pergunta
2. **📊 Decisão de Modo**: Route (simples), Coordinate (complexo), Collaborate (abrangente)
3. **🎯 Orquestração**: Direciona ou coordena especialistas apropriados
4. **🧠 Síntese**: Compila resultado contextualizado e acionável

---

## 🛠️ **CONFIGURAÇÃO INICIAL**

### 1. **Instalar Dependências**
```bash
make setup
# ou manualmente:
pip install -r requirements.txt
```

### 2. **Configurar API Keys**
```bash
cp .env.example .env
# Edite .env e configure:
GOOGLE_API_KEY=sua_google_api_key_aqui
```

### 3. **Iniciar Sistema**
```bash
make full  # Sistema completo
```

---

## 🌐 **API REST ENDPOINTS**

### **Base URL**: `http://localhost:7777`

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/v1/playground/status` | GET | Status do sistema |
| `/v1/playground/teams` | GET | Lista teams disponíveis |
| `/v1/playground/teams/{id}/runs` | POST | Executar pergunta |
| `/docs` | GET | Documentação Swagger |

### **Exemplo de Uso**
```bash
curl -X POST http://localhost:7777/v1/playground/teams/{team_id}/runs \
  -H "Content-Type: multipart/form-data" \
  -F "message=Analyze PETR4 stock performance"
```

---

## 👥 **ESPECIALISTAS DISPONÍVEIS**

### 💰 **Finance Agent**
- **Função**: Análise financeira e dados de mercado
- **Ferramentas**: yfinance, análise de ações, indicadores econômicos
- **Casos de Uso**: Preços de ações, análise econômica, tendências de mercado

### 🌐 **Web Research Agent**  
- **Função**: Pesquisas web e informações atuais
- **Ferramentas**: DuckDuckGo, scraping web, análise de conteúdo
- **Casos de Uso**: Notícias, tendências, informações em tempo real

### 💻 **Code Analysis Agent**
- **Função**: Análise e desenvolvimento de código
- **Ferramentas**: Análise estática, debugging, boas práticas
- **Casos de Uso**: Review de código, debugging, arquitetura de software

### 📊 **Data Analysis Agent**
- **Função**: Análise estatística e visualizações
- **Ferramentas**: pandas, matplotlib, estatísticas descritivas
- **Casos de Uso**: Análise de CSV, gráficos, correlações, insights

### 🐙 **GitHub Agent**
- **Função**: Integração com repositórios GitHub
- **Ferramentas**: GitHub API, análise de código, workflows
- **Casos de Uso**: Análise de repos, commits, pull requests, CI/CD

---

## 🔄 **MODOS DE OPERAÇÃO**

### 📍 **Route Mode**
- **Quando**: Tarefas simples e diretas
- **Comportamento**: Direciona para o especialista mais adequado
- **Exemplo**: "Qual o preço da PETR4?" → Finance Agent

### 🔄 **Coordinate Mode**  
- **Quando**: Tarefas complexas que requerem múltiplas perspectivas
- **Comportamento**: Orquestra vários especialistas em sequência
- **Exemplo**: "Análise completa do setor petrolífero" → Finance + Web + Data

### 🤝 **Collaborate Mode**
- **Quando**: Análises abrangentes e colaborativas
- **Comportamento**: Todos os especialistas trabalham simultaneamente
- **Exemplo**: "Estratégia completa de investimento" → Todos especialistas

---

## 📋 **COMANDOS DISPONÍVEIS**

```bash
make help      # Mostra todos os comandos
make setup     # Configura ambiente de desenvolvimento
make backend   # Executa apenas backend (porta 7777)
make frontend  # Executa apenas frontend (porta 3000) 
make full      # Executa sistema completo
make clean     # Remove arquivos temporários
```

---

## 🔧 **DESENVOLVIMENTO**

### **Estrutura do Projeto**
```
agno-teams/
├── run_backend.py          # Script backend
├── run_frontend.py         # Script frontend  
├── run_full.py            # Script completo
├── agents/                # Especialistas
│   ├── teams_manager.py   # Gerenciador de teams
│   └── specialists/       # Agentes especializados
├── tools/                 # Ferramentas dos agentes
├── config/               # Configurações
├── frontend/             # Interface Next.js + agno-ui
└── docs/                 # Documentação técnica
```

### **Adicionando Novos Especialistas**
1. Criar arquivo em `agents/specialists/`
2. Implementar função `create_*_specialist()`
3. Adicionar ao `teams_manager.py`
4. Registrar ferramentas necessárias

---

## 🚀 **DEPLOY & PRODUÇÃO**

### **Docker** (Recomendado)
```bash
docker build -t agno-teams .
docker run -p 7777:7777 -p 3000:3000 agno-teams
```

### **Servidor**
```bash
# Variáveis de ambiente em produção
export GOOGLE_API_KEY=sua_key
export HOST=0.0.0.0
export PORT=7777

# Iniciar sistema
python run_full.py
```

---

## 📊 **MONITORAMENTO**

- **Logs**: `logs/agno_playground.log`
- **Database**: `storage/agents.db`
- **Métricas**: Endpoint `/v1/playground/status`
- **Health Check**: `curl http://localhost:7777/v1/playground/status`

---

## 🛠️ **TROUBLESHOOTING**

### **Problemas Comuns**

#### ❌ "GOOGLE_API_KEY não encontrada"
```bash
# Configurar no .env
echo "GOOGLE_API_KEY=sua_key_aqui" >> .env
```

#### ❌ "Porta 7777 já em uso"
```bash
# Matar processo existente
pkill -f "python.*7777"
# ou mudar porta no .env
echo "PORT=8888" >> .env
```

#### ❌ "Frontend não conecta ao backend"
```bash
# Verificar se backend está rodando
curl http://localhost:7777/v1/playground/status
# Deve retornar: {"playground":"available"}
```

---

## 📚 **DOCUMENTAÇÃO TÉCNICA**

- **Documentação Completa**: [`docs/CONFLUENCE_DOCUMENTATION.md`](docs/CONFLUENCE_DOCUMENTATION.md)
- **API REST**: http://localhost:7777/docs (Swagger)
- **Framework Agno**: https://docs.agno.com/teams/introduction
- **Repositório**: https://github.com/diegothuran/agent-playground

---

## 📄 **LICENÇA**

MIT License - Veja arquivo LICENSE para detalhes.

---

## 🎉 **PRONTO PARA USO!**

```bash
# Configurar
make setup

# Executar sistema completo  
make full

# Acessar interface
open http://localhost:3000
```

**🚀 Agno Teams está pronto para resolver suas demandas com inteligência artificial especializada!**
