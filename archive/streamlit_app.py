#!/usr/bin/env python3
"""
🚀 Agno Teams - Frontend Streamlit

Interface web simples e eficiente para o Agno Teams Playground.
Baseado no exemplo de Agentic RAG da documentação oficial.

Uso:
streamlit run streamlit_app.py
"""

import streamlit as st
import requests
import json
import pandas as pd
import io
import time
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="🧠 Agno Teams",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações
BACKEND_URL = "http://localhost:7777"
API_BASE = f"{BACKEND_URL}/v1/playground"

class AgnoTeamsClient:
    """Cliente para comunicação com o backend Agno Teams"""
    
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
    
    def health_check(self) -> bool:
        """Verifica se o backend está rodando"""
        try:
            response = requests.get(f"{self.base_url}/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_teams(self) -> List[Dict]:
        """Busca lista de teams disponíveis"""
        try:
            response = requests.get(f"{self.base_url}/teams", timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar teams: {e}")
            return []
    
    def send_message(self, message: str, team_id: Optional[str] = None, file_data: Optional[str] = None) -> Dict:
        """Envia mensagem para o playground"""
        try:
            payload = {
                "message": message,
                "team_id": team_id,
                "file_data": file_data
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Erro {response.status_code}: {response.text}"}
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return {"error": f"Erro de conexão: {str(e)}"}

def init_session_state():
    """Inicializa estado da sessão"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "client" not in st.session_state:
        st.session_state.client = AgnoTeamsClient()
    if "selected_team" not in st.session_state:
        st.session_state.selected_team = None
    if "uploaded_file_data" not in st.session_state:
        st.session_state.uploaded_file_data = None

def render_sidebar():
    """Renderiza sidebar com configurações"""
    with st.sidebar:
        st.title("🧠 Agno Teams")
        st.markdown("Sistema inteligente de agentes especializados")
        
        # Status do backend
        if st.session_state.client.health_check():
            st.success("✅ Backend conectado")
        else:
            st.error("❌ Backend offline")
            st.warning("Execute: `make full` para iniciar o sistema")
            return
        
        # Seleção de team
        st.subheader("🎯 Teams Disponíveis")
        teams = st.session_state.client.get_teams()
        
        if teams:
            team_options = ["Auto (Route Mode)"] + [team.get("name", "Team") for team in teams]
            selected = st.selectbox(
                "Escolha um team:",
                team_options,
                index=0
            )
            
            if selected == "Auto (Route Mode)":
                st.session_state.selected_team = None
                st.info("🔄 O sistema direcionará automaticamente para o team mais adequado")
            else:
                st.session_state.selected_team = selected
                st.info(f"🎯 Usando team: {selected}")
        else:
            st.warning("Nenhum team disponível")
        
        # Upload de arquivo
        st.subheader("📁 Upload de Dados")
        uploaded_file = st.file_uploader(
            "Arraste e solte um arquivo CSV",
            type=['csv'],
            help="Faça upload de um arquivo CSV para análise"
        )
        
        if uploaded_file is not None:
            try:
                # Lê o arquivo CSV
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
                st.info(f"📊 {df.shape[0]} linhas, {df.shape[1]} colunas")
                
                # Mostra preview
                with st.expander("👀 Preview dos dados"):
                    st.dataframe(df.head())
                
                # Salva dados na sessão
                st.session_state.uploaded_file_data = df.to_csv(index=False)
                
            except Exception as e:
                st.error(f"❌ Erro ao carregar arquivo: {e}")
                st.session_state.uploaded_file_data = None
        
        # Informações adicionais
        st.subheader("ℹ️ Informações")
        with st.expander("🔧 Como usar"):
            st.markdown("""
            **Teams Disponíveis:**
            - 🔄 **Auto**: Direciona automaticamente
            - 📊 **Data Explorer**: Análise de dados
            - 💰 **Finance**: Análise financeira  
            - 🌐 **Web Research**: Pesquisa web
            - 💻 **Code**: Programação
            
            **Upload de Arquivos:**
            - Suporta arquivos CSV
            - Análise automática de dados
            - Geração de gráficos e insights
            """)
        
        with st.expander("🚀 Comandos"):
            st.markdown("""
            - `make full` - Inicia sistema completo
            - `make backend` - Só backend
            - `make frontend` - Só frontend
            """)

def render_chat():
    """Renderiza área de chat"""
    st.title("💬 Chat com Agno Teams")
    
    # Container para mensagens
    chat_container = st.container()
    
    with chat_container:
        # Exibe mensagens do histórico
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                else:
                    # Mensagem do assistente
                    if "data" in message and message["data"]:
                        # Se há dados, exibe de forma estruturada
                        response_data = message["data"]
                        
                        if "response" in response_data:
                            st.markdown(response_data["response"])
                        
                        # Exibe gráficos se houver
                        if "charts" in response_data:
                            for chart in response_data["charts"]:
                                if chart.get("type") == "plotly":
                                    st.plotly_chart(chart["data"], use_container_width=True)
                        
                        # Exibe tabelas se houver
                        if "tables" in response_data:
                            for table in response_data["tables"]:
                                st.dataframe(table, use_container_width=True)
                    else:
                        st.markdown(message["content"])
    
    # Input de mensagem
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adiciona mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Exibe mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processa resposta
        with st.chat_message("assistant"):
            with st.spinner("🤔 Pensando..."):
                # Envia para o backend
                response = st.session_state.client.send_message(
                    message=prompt,
                    team_id=st.session_state.selected_team,
                    file_data=st.session_state.uploaded_file_data
                )
                
                if "error" in response:
                    st.error(f"❌ {response['error']}")
                    content = f"Erro: {response['error']}"
                    data = None
                else:
                    # Processa resposta bem-sucedida
                    content = response.get("response", "Resposta processada com sucesso")
                    data = response
                    
                    # Exibe resposta
                    st.markdown(content)
                    
                    # Exibe dados extras se houver
                    if "charts" in response:
                        for chart in response["charts"]:
                            st.plotly_chart(chart, use_container_width=True)
                    
                    if "tables" in response:
                        for table in response["tables"]:
                            st.dataframe(table, use_container_width=True)
        
        # Salva resposta no histórico
        st.session_state.messages.append({
            "role": "assistant", 
            "content": content,
            "data": data
        })

def main():
    """Função principal"""
    init_session_state()
    
    # Layout com sidebar e área principal
    render_sidebar()
    render_chat()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            🧠 Agno Teams - Powered by <a href='https://docs.agno.com' target='_blank'>Agno Framework</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
