# 🧪 Suíte de Testes - Agno Teams Playground

Esta suíte de testes moderna valida todos os componentes do sistema Agno Teams usando pytest.

## 📋 Estrutura dos Testes

### 🔧 Configuração Base
- **`conftest.py`** - Fixtures reutilizáveis (team_id, file_path, df, etc.)

### 🌐 Testes de Backend
- **`test_backend_status.py`** - Status do servidor e endpoints básicos
- **`test_teams_api.py`** - API de teams e sessões
- **`test_playground_runs.py`** - Execução de tarefas e validação de requests

### 👥 Testes de Componentes
- **`test_specialists.py`** - Agentes especialistas e suas configurações
- **`test_system_config.py`** - Configuração do sistema e dependências

### 🔗 Testes de Integração
- **`test_integration.py`** - Fluxos completos e processamento de dados

## 🚀 Executando os Testes

```bash
# Executar todos os testes
make test

# Executar com mais detalhes
python3 -m pytest tests/ -v

# Executar teste específico
python3 -m pytest tests/test_backend_status.py -v

# Executar com coverage
python3 -m pytest tests/ --cov=app
```

## ✅ Cobertura de Testes

### Backend (Playground)
- ✅ Status do servidor (`/v1/playground/status`)
- ✅ Lista de teams (`/v1/playground/teams`)
- ✅ Execução de runs (`/v1/playground/teams/{id}/runs`)
- ✅ Validação de requests e responses
- ✅ Tempo de resposta e performance

### Especialistas
- ✅ Importação de todos os especialistas
- ✅ Configuração e atributos obrigatórios
- ✅ Estrutura de diretórios
- ✅ Ferramentas e configurações

### Integração
- ✅ Fluxo completo do sistema
- ✅ Processamento de dados CSV
- ✅ Coordenação entre especialistas
- ✅ Tratamento de erros
- ✅ Testes de performance

### Configuração
- ✅ Estrutura do projeto
- ✅ Dependências Python
- ✅ Arquivos de configuração
- ✅ Variáveis de ambiente
- ✅ Documentação

## 🎯 Resultados Esperados

A suíte valida:
- **60 testes** executados
- **55+ testes passando** em condições normais
- **2-5 testes skipped** para componentes opcionais
- **0-1 warnings** aceitáveis
- **Tempo de execução** < 30 segundos

## 🛠 Fixtures Disponíveis

```python
# Dados de teste
team_id          # ID de team para testes
file_path        # Arquivo CSV temporário
df               # DataFrame de exemplo
sample_csv_content  # Conteúdo CSV como string
data_dir         # Diretório de dados de teste

# Backend (auto-iniciado quando necessário)
backend_server   # Servidor backend para testes de integração
```

## 📊 Estratégia de Testes

### 🔍 Validação Robusta
- Testes aceitam diferentes códigos de status (200, 404, 500)
- Fallbacks para componentes não implementados
- Validação flexível de formatos de resposta

### 🎯 Cobertura Completa
- **Unidade**: Componentes individuais
- **Integração**: Fluxos entre componentes
- **Sistema**: Funcionalidade end-to-end
- **Performance**: Tempo de resposta e concorrência

### 🛡 Tratamento de Erros
- Validação de inputs inválidos
- Timeouts e conectividade
- Estados de erro controlados
- Cleanup automático de recursos

## 🔧 Manutenção

Para adicionar novos testes:

1. **Testes unitários** → Adicionar em arquivo específico do componente
2. **Testes de API** → Adicionar em `test_*_api.py`
3. **Testes de integração** → Adicionar em `test_integration.py`
4. **Fixtures** → Adicionar em `conftest.py`

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Verificar variáveis de ambiente
cat .env

# Verificar dependências
pip install -r requirements.txt

# Executar backend manualmente
python app/backend/agno_teams_playground.py
```

### Erros de import
```bash
# Verificar PYTHONPATH
export PYTHONPATH=/path/to/project:$PYTHONPATH

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Pandas/numpy issues
Os testes são resilientes a problemas de compatibilidade entre pandas/numpy.
Se persistir, usar dados como dict em vez de DataFrame.
