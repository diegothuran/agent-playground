# 🧠 Agno Teams - Documentação Técnica

## 📋 Visão Geral

O **Agno Teams** é um sistema inteligente de agentes especializados que implementa a arquitetura moderna de Teams do [Agno Framework](https://docs.agno.com). O sistema utiliza um **Team Leader** powered by **Gemini 2.0 Flash Thinking** que analisa automaticamente as solicitações e decide como orquestrar os especialistas.

## 🏗️ Arquitetura do Sistema

### Team Leader Inteligente (Gemini 2.0 Flash Thinking)

O coração do sistema é o **Team Leader** que opera em modo `coordinate`, analisando semanticamente cada solicitação e decidindo:

- **📍 Route Mode**: Para tarefas simples, direciona para 1 especialista específico
- **🔄 Coordinate Mode**: Para tarefas complexas, orquestra múltiplos agentes em pipeline
- **🤝 Collaborate Mode**: Para análises abrangentes, todos os especialistas trabalham juntos

### Especialistas Disponíveis (Gemini 2.0 Flash Thinking)

O sistema conta com 5 agentes especializados, todos utilizando **Gemini 2.0 Flash Thinking**:

#### 💰 Finance Specialist
- **Função**: Análise financeira e de mercados
- **Ferramentas**: Ferramentas financeiras simplificadas
- **Capacidades**: Análise de conceitos financeiros, interpretação de dados, recomendações

#### 🌐 Web Specialist  
- **Função**: Pesquisa web e coleta de informações
- **Ferramentas**: `DuckDuckGo` search, web research
- **Capacidades**: Pesquisa de notícias, tendências, informações atualizadas

#### 💻 Code Specialist
- **Função**: Análise e desenvolvimento de código
- **Ferramentas**: Python analysis, `flake8` style checking
- **Capacidades**: Análise de estrutura, verificação de estilo, geração de documentação

#### 📊 Data Specialist
- **Função**: Análise estatística e visualizações
- **Ferramentas**: CSV analysis, visualizações, correlações
- **Capacidades**: Análise de dados, estatísticas descritivas, insights

#### 🐙 GitHub Specialist
- **Função**: Análise de repositórios e projetos
- **Ferramentas**: GitHub insights via MCP (quando disponível)
- **Capacidades**: Análise de projetos, boas práticas, workflows

## 🚀 Implementação

### Estrutura de Arquivos

```
agno-teams/
├── backend.py              # Backend principal com Teams
├── run_backend.py          # Script para backend apenas
├── run_frontend.py         # Script para frontend apenas  
├── run_full.py            # Script para sistema completo
├── Makefile               # Comandos simplificados
├── agents/
│   ├── specialists/       # Implementações dos especialistas
│   │   ├── data_specialist.py
│   │   ├── code_specialist.py
│   │   ├── finance_specialist.py
│   │   ├── web_specialist.py
│   │   └── github_specialist.py
│   └── teams_manager.py   # Gerenciador legado (deprecated)
├── tools/                 # Ferramentas dos agentes
│   ├── data_tools_simple.py
│   ├── code_tools.py
│   ├── finance_tools.py
│   └── web_tools.py
├── frontend/              # Interface Next.js
├── config/               # Configurações
│   └── settings.py
└── docs/                 # Documentação
```

### Backend Principal (backend.py)

O arquivo `backend.py` implementa:

1. **AgnoTeamsPlayground**: Classe principal que gerencia o sistema
2. **Team Leader**: Team em modo `coordinate` que orquestra especialistas
3. **Especialistas**: Agentes com ferramentas específicas
4. **Memória Persistente**: Sistema de memória compartilhada
5. **API REST**: Playground servido via FastAPI

### Configuração de Memória

```python
# Memória persistente compartilhada
self.memory_db = SqliteMemoryDb(
    table_name="teams_memory", 
    db_file=get_storage_path("teams_memory.db")
)
self.memory = Memory(db=self.memory_db)
```

### Configuração do Team Leader

```python
config = {
    "name": "🧠 Agno Teams Leader",
    "members": specialists,  # Lista de especialistas
    "model": Gemini(id="gemini-2.0-flash-lite"),
    "description": "Team Leader inteligente...",
    "show_members_responses": True,
    "markdown": True,
    "memory": self.memory,
    "add_history_to_messages": True,
    "num_history_runs": 5,
    "enable_session_summaries": True,
}
```

## 🔌 API REST

### Endpoints Principais

| Endpoint | Método | Descrição | Exemplo |
|----------|--------|-----------|---------|
| `/v1/playground/status` | GET | Status do sistema | `{"playground": "available"}` |
| `/v1/playground/teams` | GET | Lista teams disponíveis | Array com team metadata |
| `/v1/playground/teams/{id}/runs` | POST | Nova execução | `Content-Type: multipart/form-data` |
| `/docs` | GET | Documentação Swagger | Interface interativa |

### Formato da Requisição

```bash
curl -X POST http://localhost:7777/v1/playground/teams/{team_id}/runs \
  -H "Content-Type: multipart/form-data" \
  -F "message=Sua pergunta aqui"
```

### Resposta Streaming

O sistema retorna respostas em streaming format:

```json
{
  "created_at": 1754148199,
  "event": "TeamRunResponseContent",
  "team_id": "uuid",
  "content": "Parte da resposta...",
  "content_type": "str"
}
```

## 🔄 Fluxo de Execução

### 1. Análise de Contexto

O Team Leader recebe a pergunta e:
1. Analisa o domínio (finanças, código, dados, web, github)
2. Determina a complexidade da tarefa
3. Identifica especialistas necessários

### 2. Decisão de Modo

```python
# Exemplos de decisão automática:
"Analise PETR4" → Route Mode → Finance Agent
"Crie dashboard de vendas" → Coordinate Mode → Data + Web Agents  
"Análise completa do projeto" → Collaborate Mode → Todos os agentes
```

### 3. Execução e Síntese

1. **Route**: Delega para 1 especialista
2. **Coordinate**: Orquestra pipeline de especialistas
3. **Collaborate**: Facilita colaboração entre todos
4. **Síntese**: Compila resultados em resposta contextualizada

## 🛠️ Formas de Execução

### 1. Backend Apenas

```bash
python run_backend.py
# ou
make backend
```

- **Porta**: 7777
- **Tipo**: API REST pura
- **Uso**: Integração com sistemas externos

### 2. Frontend Apenas  

```bash
python run_frontend.py
# ou
make frontend
```

- **Porta**: 3000
- **Tipo**: Interface Next.js com agno-ui
- **Pré-requisito**: Backend rodando na 7777

### 3. Sistema Completo

```bash
python run_full.py
# ou
make full
```

- **Gerência**: Backend + Frontend simultaneamente
- **Tipo**: Sistema completo para produção

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# .env
GOOGLE_API_KEY=sua_chave_gemini_aqui
```

### Dependências

```bash
# requirements.txt principais
agno>=1.7.7
google-genai
python-dotenv
uvicorn
fastapi
requests
pandas
numpy
matplotlib
duckduckgo-search
```

## 🔧 Desenvolvimento

### Adicionando Novo Especialista

1. **Criar Specialist**:
```python
# agents/specialists/new_specialist.py
def create_new_specialist() -> Agent:
    return Agent(
        name="New Specialist",
        model=Gemini(id="gemini-1.5-pro"),
        tools=[...],
        instructions=[...]
    )
```

2. **Registrar no Backend**:
```python
# backend.py - método create_specialists
new_specialist = create_new_specialist()
specialists.append(new_specialist)
```

### Adicionando Novas Ferramentas

```python
# tools/new_tools.py
class NewTools:
    def new_function(self, param: str) -> str:
        """Nova funcionalidade."""
        return f"Resultado: {param}"
```

## 🧪 Testes

### Teste Manual via cURL

```bash
# 1. Verificar status
curl http://localhost:7777/v1/playground/status

# 2. Listar teams  
curl http://localhost:7777/v1/playground/teams

# 3. Fazer pergunta
curl -X POST http://localhost:7777/v1/playground/teams/{id}/runs \
  -H "Content-Type: multipart/form-data" \
  -F "message=Teste do sistema"
```

### Teste via Interface

1. Acesse http://localhost:3000
2. Digite pergunta no chat
3. Observe orquestração automática

## 🔍 Monitoramento

### Logs

```bash
# Logs do sistema
tail -f logs/orchestrator.log

# Logs do backend
python run_backend.py  # output direto
```

### Métricas

- **Memory Usage**: Via SQLite em `storage/teams_memory.db`
- **Session History**: Histórico de 5 execuções
- **Team Performance**: Logs de coordenação

## 🚀 Deploy

### Desenvolvimento

```bash
make setup
make full
```

### Produção

```bash
# Backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend:app

# Frontend  
cd frontend && pnpm build && pnpm start
```

## 📋 Troubleshooting

### Problemas Comuns

1. **API Key inválida**:
   ```bash
   grep GOOGLE_API_KEY .env
   ```

2. **Porta ocupada**:
   ```bash
   lsof -ti:7777 | xargs kill -9
   ```

3. **Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

### Debug Mode

```python
# Ativar logs verbosos
logging.basicConfig(level=logging.DEBUG)
```

---

**📅 Última atualização**: 02/08/2025  
**🔧 Versão**: 3.0 - Arquitetura Teams simplificada  
**📖 Documentação oficial**: https://docs.agno.com/teams/introduction
