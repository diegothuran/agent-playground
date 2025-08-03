# 🚀 Agno Teams - Documentação Confluence

## 📋 **VISÃO GERAL**

Sistema moderno de agentes especializados usando o framework Agno, com arquitetura de Teams inteligente que analisa contexto e orquestra especialistas automaticamente.

---

## 🏗️ **ARQUITETURA DO SISTEMA**

### **Frontend Streamlit**
- **Tecnologia**: Streamlit moderno e responsivo
- **Funcionalidades**: Upload multi-formato, preview dinâmico, interface intuitiva
- **Formatos suportados**: CSV, PDF, XLS, XLSX via drag & drop
- **Porta**: 8501

### **Backend API REST**
- **Framework**: FastAPI + Agno Teams
- **Arquitetura**: Team Leader + Especialistas
- **Porta**: 7777
- **Documentação**: `/docs` (Swagger UI)

### **Agentes Especializados**
1. **Data Specialist**: Análise estatística e visualizações
2. **Code Specialist**: Análise e desenvolvimento de código  
3. **Finance Specialist**: Análise financeira e mercados
4. **Web Specialist**: Pesquisa web e informações online
5. **GitHub Specialist**: Integração e análise de repositórios

---

## ⚡ **OTIMIZAÇÕES DE PERFORMANCE**

### **Modelo Ultra-Otimizado**
```python
# Configuração aplicada em todos os agentes
modelo: gemini-2.0-flash-lite
temperature: 0.05 (muito baixa para respostas diretas)
max_tokens: 800 (respostas concisas)
top_p: 0.7 (determinístico)
top_k: 15 (limitado para velocidade)
```

### **AFC (Anthropic Function Calling)**
- **Status**: Habilitado por padrão
- **Configuração**: Otimizada dentro das limitações da biblioteca
- **Resultado**: Latência reduzida para máxima performance

### **Orquestração Invisível**
- **Comportamento**: Team Leader coordena especialistas silenciosamente
- **Experiência do usuário**: Vê apenas resultado final, nunca processo interno
- **Tempo de resposta**: 15-30 segundos para análises complexas

---

## 🔄 **FLUXO DE FUNCIONAMENTO**

### **1. Upload de Arquivo**
```
Usuario → Streamlit Frontend → Conversão Segura → Backend API
```

### **2. Processamento Inteligente**
```
Team Leader → Análise de Contexto → Seleção de Especialistas → Orquestração
```

### **3. Modos de Operação**
- **Route Mode**: Tarefas simples → 1 especialista
- **Coordinate Mode**: Tarefas complexas → múltiplos agentes em pipeline
- **Collaborate Mode**: Análises abrangentes → todos colaboram

### **4. Resposta Final**
```
Síntese dos Resultados → Formatação → Frontend → Usuario
```

---

## 🚀 **COMO USAR**

### **Instalação**
```bash
git clone <repositorio>
cd agno-teams
make install      # Instala dependências
make setup        # Configuração inicial
```

### **Execução**
```bash
# Modo desenvolvimento
make dev          # Backend + Frontend simultâneos

# Modo separado
make backend      # Porta 7777
make frontend     # Porta 8501
```

### **Uso no Interface**
1. **Acesse**: http://localhost:8501
2. **Upload**: Arraste arquivo (CSV/PDF/Excel) para área de upload
3. **Análise**: Digite pergunta ou solicite análise
4. **Resultado**: Receba insights processados pelos especialistas

---

## 📊 **ENDPOINTS DA API**

### **Status e Monitoramento**
- `GET /v1/playground/status` - Status do sistema
- `GET /v1/playground/teams` - Lista teams disponíveis

### **Execução de Tarefas**
- `POST /v1/playground/teams/{team_id}/runs` - Executa tarefa em team
- `GET /v1/playground/teams/{team_id}/sessions` - Lista sessões

### **Memória e Histórico**
- `GET /v1/playground/teams/{team_id}/memories` - Recupera memórias
- `DELETE /v1/playground/teams/{team_id}/sessions/{session_id}` - Limpa sessão

---

## 🔧 **CONFIGURAÇÃO TÉCNICA**

### **Variáveis de Ambiente (.env)**
```bash
# API Keys
GOOGLE_API_KEY=sua_chave_google_aqui
OPENAI_API_KEY=sua_chave_openai_aqui

# Servidor
HOST=localhost
PORT=7777

# Storage
STORAGE_DIR=storage
DB_FILE=agents.db

# MCP
MCP_ENABLED=true
MCP_SERVER_PORT=8888
```

### **Estrutura de Pastas**
```
agno-teams/
├── app/                    # Código principal
│   ├── backend/           # API REST
│   ├── frontend/          # Interface Streamlit  
│   ├── agents/            # Agentes especializados
│   ├── config/            # Configurações
│   └── tools/             # Ferramentas especializadas
├── data/                   # Dados de entrada
├── storage/               # Banco de dados
├── tests/                 # Testes automatizados
└── docs/                  # Documentação
```

---

## 🧪 **TESTES E QUALIDADE**

### **Execução de Testes**
```bash
make test         # Executa suite completa
make test-unit    # Testes unitários  
make test-api     # Testes de API
```

### **Cobertura de Testes**
- Upload multi-formato
- Processamento de dados
- Integração frontend-backend
- Resposta dos especialistas

---

## 🚨 **TROUBLESHOOTING**

### **Problemas Comuns**

#### Backend não inicia
```bash
# Verificar API key
echo $GOOGLE_API_KEY

# Verificar porta
netstat -tulpn | grep 7777
```

#### Frontend não conecta
```bash
# Verificar backend
curl http://localhost:7777/v1/playground/status

# Reiniciar frontend
make frontend
```

#### Upload falha
- Verificar tamanho do arquivo (máx 200MB)
- Verificar formato suportado (CSV/PDF/XLS/XLSX)
- Verificar encoding do CSV (UTF-8)

---

## 📈 **MÉTRICAS E MONITORAMENTO**

### **Performance**
- **Latência média**: 15-30 segundos
- **Throughput**: Processamento sequencial otimizado
- **Uso de memória**: Controlado via tokens limitados

### **Logs**
```bash
# Logs do backend
tail -f logs/orchestrator.log

# Logs dos agentes  
tail -f storage/agents.db
```

---

## 🔮 **ROADMAP FUTURO**

### **Próximas Funcionalidades**
- [ ] Suporte a mais formatos (Word, PowerPoint)
- [ ] Análise de imagens e gráficos
- [ ] Integração com mais LLMs
- [ ] Dashboard de métricas
- [ ] API de webhooks

### **Otimizações Planejadas**
- [ ] Cache inteligente de respostas
- [ ] Processamento paralelo
- [ ] Compressão de dados
- [ ] Auto-scaling horizontal

---

## 👥 **SUPORTE E CONTRIBUIÇÃO**

### **Contatos**
- **Desenvolvimento**: Time de AI/ML
- **Infraestrutura**: DevOps Team
- **Produto**: Product Owners

### **Contribuindo**
1. Fork do repositório
2. Feature branch
3. Testes passando
4. Pull request com documentação

---

**Versão**: 2.0  
**Última atualização**: 3 de agosto de 2025  
**Status**: ✅ Produção
