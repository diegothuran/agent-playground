# Agno Playground - Exemplos de Uso

Este diretório contém exemplos práticos de como usar o playground Agno para diferentes cenários.

## Exemplos Disponíveis

### `basic_usage.py` - Uso Básico
Demonstra como criar um playground simples com agentes básicos.

```bash
make example
```

### `multi_agent_conversation.py` - Conversas Multi-Agente
Mostra como fazer agentes colaborarem em tarefas complexas.

```bash
make example-multi
```

### `custom_tools_example.py` - Ferramentas Customizadas
Como criar suas próprias ferramentas para casos específicos.

```bash
make example-tools
```

### `data_analysis_workflow.py` - Análise de Dados
Fluxo completo de análise de dados usando agentes especializados.

```bash
make example-data
```

## Como Executar

Certifique-se de que o ambiente está configurado:

```bash
# No diretório raiz do projeto
make setup
make check-gemini
```

Execute qualquer exemplo:

```bash
make examples  # Lista todos os exemplos
make example   # Executa o exemplo básico
```
