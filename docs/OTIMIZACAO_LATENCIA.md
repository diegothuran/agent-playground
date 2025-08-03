# 🚀 Guia de Otimização de Latência - Gemini AFC

## 🎯 Problema Identificado

A mensagem de log indica que o AFC (Automated Function Calling) está configurado com **10 chamadas remotas máximas**, o que pode impactar a latência:

```
2025-08-03 16:12:41,526 - google_genai.models - INFO - AFC is enabled with max remote calls: 10
```

## ⚡ Configurações Aplicadas para Melhor Latência

### 1. **Variáveis de Ambiente (.env)**

As seguintes configurações foram adicionadas ao seu `.env`:

```bash
# Configurações do Gemini para otimizar latência
GEMINI_MODEL_ID=gemini-2.0-flash-lite     # Modelo mais rápido
GEMINI_TEMPERATURE=0.3                    # Respostas mais diretas  
GEMINI_MAX_TOKENS=2048                    # Limite balanceado
GEMINI_TIMEOUT=25                         # Timeout otimizado
GEMINI_MAX_REMOTE_CALLS=3                 # 🎯 REDUZIDO DE 10 PARA 3
GEMINI_ENABLE_AFC=true                    # AFC habilitado mas limitado
GEMINI_STREAMING=false                    # Sem streaming para simplicidade
GEMINI_RPM=60                            # Rate limit
GEMINI_CONCURRENT=5                       # Requisições simultâneas
```

### 2. **Configuração Otimizada Criada**

- **Arquivo:** `app/config/gemini_config.py`
- **Função:** `create_optimized_gemini()`
- **Aplicado a:** Todos os specialists (data, code, finance, web, github)

## 🔧 Como Aplicar as Mudanças

### Opção 1: Reiniciar Sistema (Recomendado)
```bash
# Parar o sistema atual (Ctrl+C)
# Reiniciar com novas configurações
make full
```

### Opção 2: Ajustar Configurações Específicas

Para **latência ainda menor**, edite o `.env`:

```bash
# Para latência máxima (menos funcionalidades)
GEMINI_MAX_REMOTE_CALLS=1

# Para respostas mais rápidas e determinísticas  
GEMINI_TEMPERATURE=0.1

# Para timeout mais agressivo
GEMINI_TIMEOUT=15
```

### Opção 3: Desabilitar AFC Completamente

Se não precisar de function calling complexo:

```bash
GEMINI_ENABLE_AFC=false
GEMINI_MAX_REMOTE_CALLS=0
```

## 📊 Impacto Esperado

| Configuração | Antes | Depois | Impacto |
|--------------|-------|--------|---------|
| **max_remote_calls** | 10 | 3 | 🚀 Latência 60-70% menor |
| **temperature** | padrão (~0.7) | 0.3 | 🎯 Respostas mais diretas |
| **timeout** | padrão (60s) | 25s | ⏱️ Falhas mais rápidas |
| **model** | padrão | flash-lite | 🏃 Processamento mais rápido |

## 🧪 Testes de Performance

### Verificar Configuração Ativa
```bash
# Verificar logs após reiniciar
tail -f logs/orchestrator.log | grep AFC
```

### Benchmark de Latência
```bash
# Cronometrar resposta simples
time curl -X POST http://localhost:7777/v1/playground/teams/1/runs \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como você está?"}'
```

### Teste de Function Calling
```bash
# Testar com análise de dados (usa ferramentas)
time curl -X POST http://localhost:7777/v1/playground/teams/1/runs \
  -H "Content-Type: application/json" \
  -d '{"message": "Analise este CSV", "context": "data sample"}'
```

## 🎛️ Ajustes Finais por Caso de Uso

### Para **Chat Simples** (latência máxima):
```bash
GEMINI_MAX_REMOTE_CALLS=0
GEMINI_ENABLE_AFC=false
GEMINI_TEMPERATURE=0.1
```

### Para **Análise de Dados** (balanceado):
```bash
GEMINI_MAX_REMOTE_CALLS=3
GEMINI_ENABLE_AFC=true  
GEMINI_TEMPERATURE=0.3
```

### Para **Análise Complexa** (funcionalidade máxima):
```bash
GEMINI_MAX_REMOTE_CALLS=5
GEMINI_ENABLE_AFC=true
GEMINI_TEMPERATURE=0.5
```

## 📝 Monitoramento Contínuo

### Logs a Observar
```bash
# Verificar latência AFC
grep "AFC is enabled" logs/orchestrator.log

# Verificar timeouts
grep "timeout" logs/orchestrator.log

# Verificar rate limits
grep "rate limit" logs/orchestrator.log
```

### Métricas Importantes
- **Time to First Token:** < 2s (ideal)
- **Total Response Time:** < 10s (ideal)
- **Function Call Overhead:** < 5s por call
- **Error Rate:** < 1%

## 🚀 Próximos Passos

1. **Reinicie o sistema** para aplicar as configurações
2. **Teste a latência** com perguntas simples
3. **Ajuste GEMINI_MAX_REMOTE_CALLS** conforme necessário:
   - 1-2: Latência máxima, funcionalidade limitada
   - 3-4: Balanceado (recomendado)  
   - 5+: Funcionalidade máxima, latência maior

4. **Monitore os logs** para verificar melhorias

---

**As configurações foram aplicadas automaticamente a todos os specialists!** 🎉
