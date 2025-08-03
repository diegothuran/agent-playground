# 🧠 Agno Teams - Sistema de Agentes Especializados

Sistema moderno de agentes especializados usando o framework Agno, com arquitetura de Teams inteligente que analisa contexto e orquestra especialistas automaticamente.

## 📁 Estrutura do Projeto

```
📦 agno-teams/
├── 📄 main.py                    # Ponto de entrada principal
├── 📄 Makefile                   # Comandos de automação
├── 📄 requirements.txt           # Dependências Python
├── 📄 README.md                  # Esta documentação
├── 📄 LICENSE                    # Licença do projeto
│
├── 📁 app/                       # Código principal da aplicação
│   ├── 📁 backend/              # Backend API REST
│   │   └── agno_teams_playground.py
│   ├── 📁 frontend/             # Frontend Streamlit
│   │   └── streamlit_frontend.py
│   ├── 📁 scripts/              # Scripts de execução
│   │   ├── run_backend.py
│   │   ├── run_frontend.py
│   │   ├── run_streamlit_frontend.py
│   │   └── run_full_streamlit.py
│   ├── 📁 agents/               # Agentes especializados
│   │   ├── orchestrator_agent.py
│   │   ├── data_agent.py
│   │   ├── finance_agent.py
│   │   ├── github_agent.py
│   │   └── ...
│   ├── 📁 config/               # Configurações
│   │   └── settings.py
│   ├── 📁 mcp/                  # Model Context Protocol
│   │   ├── data_exploration_mcp.py
│   │   └── github_mcp.py
│   ├── 📁 tools/                # Ferramentas auxiliares
│   ├── 📁 examples/             # Exemplos de uso
│   └── 📁 __pycache__/
│
├── 📁 data/                     # Dados e arquivos
│   ├── 📁 samples/              # Arquivos de exemplo
│   │   ├── vendas_exemplo.csv
│   │   ├── acoes_exemplo.csv
│   │   └── test_upload.csv
│   └── 📁 storage/              # Banco de dados
│       └── agents.db
│
├── 📁 tests/                    # Testes automatizados
│   ├── test_multi_format.py
│   ├── test_csv_upload.py
│   └── ...
│
├── 📁 docs/                     # Documentação
│   ├── MULTI_FORMAT_UPLOAD.md
│   └── README_NEW.md
│
└── 📁 archive/                  # Arquivos antigos/backup
    ├── frontend/                # Frontend Next.js antigo
    └── ...
```

## 🚀 Início Rápido

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone <repository-url>
cd agno-teams

# Configure o ambiente
make setup
```

### 2. Execução

**Sistema Completo (Recomendado):**
```bash
make full
# ou
python main.py --mode full
```

**Apenas Backend:**
```bash
make backend
# ou  
python main.py --mode backend
```

**Apenas Frontend:**
```bash
make frontend
# ou
python main.py --mode frontend
```

### 3. Acesso

- **Frontend Streamlit:** http://localhost:8501
- **Backend API:** http://localhost:7777
- **Documentação API:** http://localhost:7777/docs

## 🌟 Funcionalidades

### 📊 Upload Multi-Formato
- **CSV:** Análise de dados tabulares
- **PDF:** Extração e análise de documentos
- **Excel (XLS/XLSX):** Planilhas e relatórios
- **Preview em tempo real** antes do envio

### 🤖 Agentes Especializados
- **Data Agent:** Análise de dados e visualizações
- **Finance Agent:** Métricas financeiras e investimentos
- **GitHub Agent:** Análise de repositórios e código
- **Web Agent:** Pesquisa e análise web
- **Orchestrator:** Coordenação inteligente entre agentes

### 🔗 Integração MCP
- **Data Exploration:** Análise avançada de dados
- **GitHub Integration:** Conecta com repositórios
- **Extensibilidade:** Fácil adição de novos MCPs

## 📝 Como Usar

### 1. Upload de Arquivos
1. Acesse http://localhost:8501
2. Arraste arquivos para a área de upload
3. Visualize o preview automático
4. Faça perguntas sobre seus dados

### 2. Análise de Dados
```
Exemplo de perguntas:
- "Analise as vendas por região"
- "Quais são os principais insights financeiros?"
- "Crie gráficos das tendências"
- "Compare performance dos produtos"
```

### 3. API REST
```bash
# Status do sistema
curl http://localhost:7777/v1/playground/status

# Listar teams
curl http://localhost:7777/v1/playground/teams

# Executar análise
curl -X POST http://localhost:7777/v1/playground/teams/1/runs \
  -H "Content-Type: application/json" \
  -d '{"message": "Analise os dados", "context": "..."}'
```

## 🧪 Testes

```bash
# Executar todos os testes
make test

# Testes específicos
python -m pytest tests/test_multi_format.py -v
python -m pytest tests/test_csv_upload.py -v
```

## 🛠️ Desenvolvimento

### Estrutura de Comandos
```bash
make help      # Mostrar ajuda
make setup     # Configurar ambiente
make backend   # Apenas backend
make frontend  # Apenas frontend  
make full      # Sistema completo
make test      # Executar testes
make clean     # Limpeza
```

### Adicionando Novos Agentes
1. Crie arquivo em `app/agents/`
2. Implemente interface base do agente
3. Registre no orchestrador
4. Adicione testes em `tests/`

### Adicionando Novos MCPs
1. Crie arquivo em `app/mcp/`
2. Implemente protocolo MCP
3. Configure em `app/config/`
4. Teste integração

## 📚 Documentação

- **Upload Multi-Formato:** `docs/MULTI_FORMAT_UPLOAD.md`
- **Guia de Desenvolvimento:** `docs/README_NEW.md`
- **API Reference:** http://localhost:7777/docs (quando rodando)

## 🔧 Troubleshooting

### Problemas Comuns

**Backend não inicia:**
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar porta
lsof -i :7777
```

**Frontend não conecta:**
```bash
# Verificar se backend está rodando
curl http://localhost:7777/v1/playground/status

# Verificar logs do Streamlit
```

**Erro de import:**
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 📄 Licença

[LICENSE](LICENSE)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Desenvolvido com ❤️ usando Agno Framework + Streamlit**
