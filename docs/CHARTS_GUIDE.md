# 📊 Guia: Como Plotar Gráficos no Frontend

## ✅ Sistema Implementado

O **Agno Playground** agora possui um sistema **automático** de detecção e exibição de gráficos! 

### 🔧 Como Funciona

1. **Backend (Python)** - As ferramentas de dados geram gráficos em base64:
   ```python
   # tools/data_tools.py
   def create_visualization(self, data, chart_type="line"):
       # ... gera matplotlib plot ...
       buffer = io.BytesIO()
       plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
       image_base64 = base64.b64encode(buffer.getvalue()).decode()
       return f"data:image/png;base64,{image_base64}"
   ```

2. **Frontend (Next.js)** - Detecta automaticamente URLs de imagem base64:
   ```tsx
   // ChartDisplay.tsx
   const base64ImageRegex = /data:image\/[a-zA-Z]*;base64,([^)]*)/g
   const matches = content.match(base64ImageRegex)
   ```

3. **Integração Automática** - Qualquer resposta do agente que contenha `data:image/png;base64,` será automaticamente detectada e exibida como gráfico.

### 🎯 Exemplo de Uso

**Pergunte ao agente:**
```
"Crie um gráfico de linha com os dados [1, 2, 3, 4, 5]"
```

**O agente automaticamente:**
1. Usa a ferramenta `create_visualization` 
2. Gera o gráfico em base64
3. Inclui o base64 na resposta
4. O frontend detecta e exibe o gráfico

### 📈 Tipos de Gráficos Suportados

- **📈 Line** - `chart_type="line"` 
- **📊 Bar** - `chart_type="bar"`
- **📉 Scatter** - `chart_type="scatter"`
- **📋 Histogram** - `chart_type="histogram"`
- **🔥 Heatmap** - `chart_type="correlation"` (via `create_advanced_visualization`)
- **📦 Box Plot** - `chart_type="box"`
- **📊 Distribution** - `chart_type="distribution"`

### 🚀 Exemplos Práticos

#### 1. Gráfico Simples
```
"Crie um gráfico de barras com vendas: Janeiro=100, Fevereiro=150, Março=200"
```

#### 2. Análise de CSV
```
"Carregue o arquivo vendas.csv e crie gráficos de tendência"
```

#### 3. Análise Avançada
```
"Analise correlações no dataset clientes.csv e mostre uma matriz de correlação"
```

### ✨ Recursos do Frontend

- **🎨 Design Responsivo** - Gráficos se adaptam ao tamanho da tela
- **🔍 Hover Effects** - Efeitos visuais ao passar o mouse
- **📱 Mobile-Friendly** - Funciona perfeitamente em dispositivos móveis
- **🎯 Auto-Detection** - Detecção automática sem configuração manual
- **🔄 Error Handling** - Fallback gracioso se o gráfico não carregar

### 🎮 Testando o Sistema

1. **Inicie o playground:**
   ```bash
   make dev-orchestrated
   ```

2. **Acesse o frontend:**
   ```
   http://localhost:3000
   ```

3. **Teste com uma pergunta:**
   ```
   "Crie um gráfico de linha com os números 10, 20, 30, 40, 50"
   ```

4. **Veja o gráfico aparecer automaticamente!** 📊

### 🔧 Arquivos Modificados

- ✅ `frontend/src/components/playground/ChatArea/Messages/Charts/` - Componente de exibição
- ✅ `frontend/src/components/playground/ChatArea/Messages/MessageItem.tsx` - Integração automática
- ✅ `tools/data_tools.py` - Geração de gráficos base64
- ✅ `agents/orchestrator_agent.py` - Ferramentas de dados integradas

### 🎉 Resultado

Agora você tem um sistema **100% automático** onde:

1. **Usuário pergunta** sobre dados
2. **Agente analisa** e decide usar ferramentas de visualização  
3. **Backend gera** gráficos em base64
4. **Frontend detecta** e exibe automaticamente
5. **Usuário vê** gráficos lindos e interativos! 

**🎯 Nenhuma configuração manual necessária - tudo funciona automaticamente!**
