# 🔗 Guia de MCPs (Model Context Protocol)

## 📋 O que são MCPs?

Model Context Protocol (MCP) é um protocolo que permite aos agentes de IA se conectarem e interagirem com sistemas externos de forma padronizada. No Agno Playground, os MCPs permitem que o assistente acesse APIs externas, bancos de dados, e outros serviços.

## 🚀 MCPs Disponíveis

### 1. GitHub MCP

Integração com a API do GitHub para buscar repositórios, issues, e informações de usuários.

**Configuração:**
```bash
# Adicione ao .env
GITHUB_TOKEN=seu_token_github_aqui
```

**Funcionalidades:**
- 🔍 Buscar repositórios por palavras-chave
- 📊 Obter informações detalhadas de repositórios
- 🐛 Listar issues abertas/fechadas
- 👤 Informações de perfis de usuários

**Exemplos de uso:**
```text
"Busque repositórios Python sobre machine learning"
"Mostre informações do repositório facebook/react"
"Quais issues estão abertas no projeto microsoft/vscode?"
"Informações sobre o usuário torvalds no GitHub"
```

### 2. MCP Genérico

Sistema base para conectar com qualquer API REST.

**Funcionalidades:**
- 🌐 Registrar novos servidores MCP
- 📡 Fazer chamadas HTTP para APIs
- 🔍 Verificar status de serviços
- 📝 Logs de conexão

### 2. Exploração Avançada de Dados MCP

Integração com ferramentas avançadas de análise de dados baseadas no mcp-server-data-exploration.

**Funcionalidades:**
- 📊 Carregamento de CSV de qualquer tamanho (até 200MB)
- 🐍 Execução de scripts Python personalizados
- 📈 Análise exploratória automática
- 🎨 Geração de visualizações e gráficos
- 📋 Análise estatística completa

**Exemplos de uso:**
```text
"Analise o dataset vendas.csv focando em padrões sazonais"
"Explore correlações entre todas as variáveis do arquivo dados.csv"
"Crie visualizações das tendências de temperatura ao longo do tempo"
"Execute análise de outliers nos dados financeiros"
"Gere relatório completo de análise exploratória"
```

**Casos de uso demonstrados:**
- 🏠 Análise de preços imobiliários na Califórnia (2.2M+ registros)
- 🌤️ Padrões meteorológicos em Londres (2.8M+ registros)
- 🛒 Dados de vendas de e-commerce
- 📊 Qualquer dataset em formato CSV

## 🛠️ Como Adicionar um Novo MCP

### Passo 1: Configurar no `mcp/config.json`

```json
{
  "servers": {
    "seu_mcp": {
      "name": "Seu Novo MCP",
      "url": "api.exemplo.com",
      "port": 443,
      "protocol": "https",
      "description": "Descrição do seu MCP",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN",
        "Accept": "application/json"
      },
      "endpoints": [
        "/endpoint1",
        "/endpoint2"
      ]
    }
  }
}
```

### Passo 2: Criar Ferramentas Especializadas

Crie um arquivo `mcp/seu_mcp.py`:

```python
from mcp.mcp_tools import MCPTools

class SeuMCPTools(MCPTools):
    def __init__(self, token=None):
        super().__init__()
        self.base_url = "https://api.exemplo.com"
        # Configure headers, autenticação, etc.
    
    def sua_funcao(self, parametros):
        # Implemente suas funções específicas
        pass
```

### Passo 3: Adicionar ao Orquestrador

No `agents/orchestrator_agent.py`:

```python
# Importação condicional
try:
    from mcp.seu_mcp import SeuMCPTools
    SEU_MCP_AVAILABLE = True
except ImportError:
    SEU_MCP_AVAILABLE = False

# Na função create_orchestrator_agent:
if SEU_MCP_AVAILABLE:
    seu_mcp = SeuMCPTools()
    all_tools.extend([
        seu_mcp.sua_funcao
    ])
```

### Passo 4: Atualizar Variáveis de Ambiente

No `.env.example`:

```bash
# Seu MCP
SEU_MCP_TOKEN=seu_token_aqui
```

### Passo 5: Criar Exemplo de Uso

Crie `examples/seu_mcp_example.py` com exemplos práticos.

## 🔧 Troubleshooting

### Erro: "MCP não disponível"

1. Verifique se o arquivo Python do MCP está criado
2. Confirme que as dependências estão instaladas
3. Verifique se o token/chave de API está configurado

### Erro: "API rate limit"

1. Verifique os limites da API externa
2. Implemente cache se necessário
3. Adicione delays entre chamadas

### Erro: "Conexão falhou"

1. Verifique conectividade de rede
2. Confirme URL e porta da API
3. Teste autenticação manualmente

## 📚 Exemplos de MCPs Úteis

### APIs Populares para Integrar:

- **Slack API** - Enviar mensagens, listar canais
- **Discord API** - Interagir com servidores Discord
- **Twitter API** - Buscar tweets, dados de usuários
- **Weather API** - Dados meteorológicos
- **News APIs** - Notícias em tempo real
- **Database APIs** - Consultas a bancos de dados

### Template Genérico:

```python
class NovoMCPTools(MCPTools):
    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://api.exemplo.com/v1"
        
    def funcao_principal(self, query: str) -> dict:
        # Implementar lógica específica
        return {"status": "success", "data": "resultado"}
```

## 🎯 Melhores Práticas

1. **Tratamento de Erros**: Sempre implemente try/catch adequado
2. **Rate Limiting**: Respeite limites das APIs externas
3. **Cache**: Implemente cache para dados que mudam pouco
4. **Documentação**: Documente parâmetros e retornos
5. **Testes**: Crie testes para suas funções MCP
6. **Segurança**: Nunca hardcode tokens ou senhas

## 🔍 Monitoramento

Use `check_mcp_health()` para monitorar status dos MCPs:

```python
# Verificar todos os MCPs
assistant.run("Verifique o status de todos os MCPs")

# Verificar MCP específico
assistant.run("Status do GitHub MCP")
```

---

**💡 Dica**: O assistente orquestrador escolhe automaticamente qual MCP usar baseado no contexto da pergunta. Você não precisa especificar qual MCP quer usar!
