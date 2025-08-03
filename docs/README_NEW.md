# 🧠 Agno Teams - Sistema de Agentes Especializados

Sistema moderno de agentes especializados usando o framework Agno, com arquitetura de Teams inteligente que analisa contexto e orquestra especialistas automaticamente.

## 🏗️ **Estrutura do Projeto**

```
agno-teams/
├── 📁 src/                          # Código fonte principal
│   ├── agno_teams_playground.py     # Backend principal (API Teams)
│   ├── streamlit_frontend.py        # Frontend Streamlit multi-formato
│   ├── run_backend.py               # Script para backend apenas
│   ├── run_frontend.py              # Script para frontend apenas
│   ├── run_streamlit_frontend.py    # Script para Streamlit
│   └── run_full_streamlit.py        # Script para sistema completo
├── 📁 agents/                       # Agentes especializados
├── 📁 config/                       # Configurações
├── 📁 docs/                         # Documentação técnica
├── 📁 tools/                        # Ferramentas dos agentes
├── 📁 tests/                        # Testes automatizados
├── 📁 samples/                      # Arquivos de exemplo
├── 📁 storage/                      # Banco de dados e memória
├── 📁 archive/                      # Arquivos antigos
├── main.py                          # Ponto de entrada principal
├── Makefile                         # Comandos simplificados
└── requirements.txt                 # Dependências
```

## 🚀 **Execução Rápida**

### **Método 1: Arquivo Principal**
```bash
# Sistema completo
python main.py

# Apenas backend
python main.py --mode backend

# Apenas frontend
python main.py --mode frontend
```

### **Método 2: Comandos Make**
```bash
# Configuração inicial
make setup

# 3 formas de execução
make backend    # Backend apenas (porta 7777)
make frontend   # Frontend Streamlit (porta 8501)
make full       # Sistema completo

# Manutenção
make test       # Executar testes
make clean      # Limpeza
```

## 🎯 **Funcionalidades**

### **Frontend Streamlit Multi-Formato**
- 📊 **CSV**: Análise de dados tabulares
- 📄 **PDF**: Extração de texto e documentos
- 📈 **Excel (XLS/XLSX)**: Planilhas com múltiplas abas
- 🎨 **Interface moderna**: Chat inteligente com upload drag & drop

### **Team Leader Inteligente**
- 🧠 **Análise de contexto**: Compreende automaticamente a solicitação
- 🎯 **Orquestração inteligente**: Escolhe e coordena especialistas
- 📊 **3 modos de operação**: Route, Coordinate, Collaborate

### **Especialistas Disponíveis**
- 💰 **Finance Specialist**: Análise financeira e mercados
- 🌐 **Web Specialist**: Pesquisa web e informações online
- 💻 **Code Specialist**: Análise e desenvolvimento de código
- 📊 **Data Specialist**: Análise estatística e visualizações
- 🐙 **GitHub Specialist**: Integração e análise de repositórios

## 📋 **API REST Endpoints**

**Base URL**: `http://localhost:7777`

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/v1/playground/status` | GET | Status do sistema |
| `/v1/playground/teams` | GET | Lista teams disponíveis |
| `/v1/playground/teams/{id}/runs` | POST | Executar pergunta |
| `/docs` | GET | Documentação Swagger |

## 🛠️ **Configuração Inicial**

```bash
# 1. Clonar e entrar no projeto
cd agno-teams/

# 2. Instalar dependências
make setup
# ou
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API

# 4. Executar
make full
```

## 🌐 **Acesso ao Sistema**

- **🎨 Frontend**: http://localhost:8501
- **🔗 Backend API**: http://localhost:7777
- **📋 Documentação**: http://localhost:7777/docs

## 🧪 **Desenvolvimento e Testes**

```bash
# Executar testes
make test

# Limpeza do projeto
make clean

# Estrutura de testes
tests/
├── test_backend.py
├── test_frontend.py
├── test_multi_format.py
└── test_agents.py
```

## 📚 **Documentação Técnica**

- **[Documentação Completa](docs/CONFLUENCE_DOCUMENTATION.md)** - Guia técnico detalhado
- **[Guia de Upload](MULTI_FORMAT_UPLOAD.md)** - Suporte multi-formato
- **[Guia MCP](docs/MCP_GUIDE.md)** - Model Context Protocol
- **[Guia de Gráficos](docs/CHARTS_GUIDE.md)** - Visualizações

## 🔧 **Troubleshooting**

### Problemas Comuns

**Backend não inicia:**
```bash
# Verificar porta
lsof -i :7777

# Verificar dependências
pip install -r requirements.txt
```

**Frontend não carrega:**
```bash
# Verificar se backend está rodando
curl http://localhost:7777/v1/playground/status

# Reiniciar frontend
make frontend
```

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**⚡ Sistema otimizado, organizado e pronto para produção!**
