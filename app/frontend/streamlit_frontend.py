import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import io
import time
import base64
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

# Imports locais
from session_manager import get_session_manager

# Configuração da página
st.set_page_config(
    page_title="🧠 Agno Teams Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações
BACKEND_URL = "http://localhost:7777"

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CSS customizado com alto contraste para melhor legibilidade
st.markdown("""
<style>
    /* FORÇA TEXTO ESCURO EM TODOS OS ELEMENTOS */
    * {
        color: #000000 !important;
    }
    
    /* Reset e configurações globais */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* FORÇA texto escuro em todos os elementos Streamlit */
    .main .block-container {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Sidebar com fundo claro e texto escuro */
    .css-1d391kg, .css-17eq0hr, .sidebar .sidebar-content {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border-right: 2px solid #dee2e6;
    }
    
    /* Títulos e headers SEMPRE escuros */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Texto geral SEMPRE escuro */
    .stMarkdown, .stText, p, span, div {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* Labels e descrições */
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Remover margens padrão do Streamlit */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 95%;
        background-color: #ffffff !important;
    }
    
    /* Estilo para drag & drop com maior contraste */
    .uploadedFile {
        border: 3px dashed #000000 !important;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin: 15px 0;
        background-color: #f8f9fa !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    .uploadedFile:hover {
        border-color: #0d6efd !important;
        background-color: #e7f1ff !important;
        color: #000000 !important;
    }
    
    /* Estilo para sessões com melhor contraste */
    .session-item {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        border-left: 5px solid #0d6efd;
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .session-item:hover {
        background-color: #f8f9fa !important;
        border-color: #0d6efd !important;
        cursor: pointer;
        color: #000000 !important;
    }
    
    .session-active {
        background-color: #d1e7dd !important;
        border-left-color: #198754;
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Estilo para mensagens do usuário */
    .user-message {
        background-color: #cfe2ff !important;
        padding: 18px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #0d6efd;
        border: 3px solid #0d6efd !important;
        color: #000000 !important;
    }
    
    /* Estilo para mensagens do assistente */
    .assistant-message {
        background-color: #d1e7dd !important;
        padding: 18px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #198754;
        border: 3px solid #198754 !important;
        color: #000000 !important;
    }
    
    .message-content {
        line-height: 1.7;
        font-size: 16px !important;
        margin: 10px 0;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .message-timestamp {
        font-size: 14px !important;
        color: #333333 !important;
        margin-top: 10px;
        font-weight: 600 !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid #666666;
    }
    
    /* Indicador de carregamento */
    .loading-indicator {
        padding: 18px;
        background-color: #fff3cd !important;
        border: 3px solid #000000 !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Botões com cores escuras e texto branco */
    .stButton > button {
        border: 3px solid #000000 !important;
        background-color: #000000 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    
    .stButton > button:hover {
        background-color: #333333 !important;
        color: #ffffff !important;
    }
    
    /* Inputs com fundo branco e texto preto */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 3px solid #000000 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    
    /* Selectbox com texto escuro */
    .stSelectbox > div > div > select {
        background-color: #ffffff !important;
        border: 3px solid #000000 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    
    /* Alertas com texto escuro */
    .stAlert {
        border: 3px solid #000000 !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }
    
    .stSuccess {
        background-color: #d1e7dd !important;
        color: #000000 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        color: #000000 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        color: #000000 !important;
    }
    
    .stInfo {
        background-color: #cfe2ff !important;
        color: #000000 !important;
    }
    
    /* FORÇA qualquer texto a ser preto */
    .element-container, .stMarkdown, .stSelectbox, .stTextInput, .stTextArea {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)
        transform: translateX(3px);
        transition: all 0.2s ease;
    }
    
    .session-active {
        background-color: #d1e7dd;
        border-left-color: #198754;
        color: #0f5132;
        font-weight: 600;
    }
    
    /* Estilo para mensagens do usuário - azul com alto contraste */
    .user-message {
        background-color: #cfe2ff;
        padding: 18px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #0d6efd;
        border: 2px solid #b6d4fe;
        box-shadow: 0 3px 6px rgba(13, 110, 253, 0.15);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #052c65;
    }
    
    /* Estilo para mensagens do assistente - verde com alto contraste */
    .assistant-message {
        background-color: #d1e7dd;
        padding: 18px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #198754;
        border: 2px solid #a3cfbb;
        box-shadow: 0 3px 6px rgba(25, 135, 84, 0.15);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #0f5132;
    }
    
    .message-content {
        line-height: 1.7;
        font-size: 15px;
        margin: 10px 0;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: pre-wrap;
        color: inherit;
        font-weight: 500;
    }
    
    .message-timestamp {
        font-size: 13px;
        color: #6c757d;
        margin-top: 10px;
        opacity: 1;
        font-style: italic;
        font-weight: 500;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
    }
    
    /* Indicador de carregamento com cores mais vibrantes */
    .loading-indicator {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 18px;
        background-color: #fff3cd;
        border-radius: 10px;
        margin: 15px 0;
        border: 2px solid #ffc107;
        color: #664d03;
        font-weight: 600;
        box-shadow: 0 3px 6px rgba(255, 193, 7, 0.2);
    }
    
    .spinner {
        border: 3px solid #f8f9fa;
        border-top: 3px solid #0d6efd;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Melhorar aparência dos botões com maior contraste */
    .stButton > button {
        border-radius: 8px;
        border: 2px solid #0d6efd;
        background-color: #0d6efd;
        color: #ffffff;
        font-weight: 600;
        padding: 8px 16px;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .stButton > button:hover {
        background-color: #0b5ed7;
        border-color: #0a58ca;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(13, 110, 253, 0.3);
    }
    
    /* Melhorar contraste dos inputs */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #ced4da;
        color: #212529;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0d6efd;
        box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
    }
    
    /* Melhorar contraste dos selectbox */
    .stSelectbox > div > div > select {
        background-color: #ffffff;
        border: 2px solid #ced4da;
        color: #212529;
        font-weight: 500;
    }
    
    /* Estilo para métricas */
    .metric-container {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 12px;
        color: #212529;
        font-weight: 600;
    }
    
    /* Texto em headers e títulos com melhor contraste */
    h1, h2, h3, h4, h5, h6 {
        color: #212529 !important;
        font-weight: 700 !important;
    }
    
    /* Texto geral */
    .stMarkdown, .stText {
        color: #212529;
        font-weight: 500;
    }
    
    /* Melhorar contraste nos alertas */
    .stAlert {
        border-radius: 8px;
        border: 2px solid;
        font-weight: 600;
    }
    
    .stSuccess {
        background-color: #d1e7dd;
        border-color: #198754;
        color: #0f5132;
    }
    
    .stError {
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    
    .stWarning {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #664d03;
    }
    
    .stInfo {
        background-color: #cfe2ff;
        border-color: #0d6efd;
        color: #052c65;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Inicializa estado da sessão com melhorias."""
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = get_session_manager()
    
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "uploaded_file_data" not in st.session_state:
        st.session_state.uploaded_file_data = None
    
    if "selected_team_id" not in st.session_state:
        st.session_state.selected_team_id = None
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    if "last_processing_time" not in st.session_state:
        st.session_state.last_processing_time = None

@st.cache_data(ttl=30)  # Cache por 30 segundos
def check_backend_health():
    """Verifica se o backend está rodando com cache."""
    try:
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=5)
        return response.status_code == 200
    except:
        return False

@st.cache_data(ttl=60)  # Cache por 1 minuto
def get_teams():
    """Busca lista de teams disponíveis com cache."""
    try:
        response = requests.get(f"{BACKEND_URL}/v1/playground/teams", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Erro ao buscar teams: {e}")
        return []

def load_session_messages(session_id: str):
    """Carrega mensagens de uma sessão."""
    if session_id:
        messages = st.session_state.session_manager.get_session_messages(session_id)
        st.session_state.messages = [
            {
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["timestamp"]
            }
            for msg in messages
        ]
    else:
        st.session_state.messages = []

def create_new_session():
    """Cria uma nova sessão."""
    session_name = f"Nova Sessão {datetime.now().strftime('%d/%m %H:%M')}"
    session_id = st.session_state.session_manager.create_session(
        name=session_name,
        team_id=st.session_state.selected_team_id
    )
    st.session_state.current_session_id = session_id
    st.session_state.messages = []
    st.rerun()

def send_message_to_team(message: str, team_id: str, file_content: Optional[str] = None):
    """Envia mensagem para um team específico com melhorias."""
    try:
        enhanced_message = message
        
        # Processar arquivo anexado
        if file_content:
            try:
                file_data = json.loads(file_content)
                filename = file_data.get('filename', 'arquivo')
                file_type = file_data.get('type', 'unknown')
                
                if file_type == 'csv':
                    enhanced_message = f"{message}\n\n📊 **Arquivo CSV anexado**: {filename}\n```csv\n{file_data['content'][:2000]}...\n```\n\nPor favor, analise este dataset CSV completo."
                
                elif file_type == 'pdf':
                    enhanced_message = f"{message}\n\n📄 **Arquivo PDF anexado**: {filename}\n[Conteúdo em Base64 - {file_data['size']} bytes]\n\nPor favor, extraia e analise o texto deste PDF."
                
                elif file_type in ['xls', 'xlsx']:
                    enhanced_message = f"{message}\n\n📊 **Planilha Excel anexada**: {filename}\n[Arquivo {file_type.upper()} em Base64 - {file_data['size']} bytes]\n\nPor favor, processe esta planilha e analise os dados."
                
            except (json.JSONDecodeError, KeyError):
                enhanced_message = f"{message}\n\nArquivo CSV carregado para análise:\n```csv\n{file_content[:2000]}...\n```"
        
        # Preparar dados da requisição
        files = {
            'message': (None, enhanced_message),
            'stream': (None, 'false')
        }
        
        # Enviar para o team específico
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
                files=files,
                timeout=180  # Timeout de 3 minutos
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Processar resposta
                if isinstance(result, dict):
                    content = result.get("content", str(result))
                    return {"response": content}
                elif isinstance(result, list):
                    full_content = ""
                    for event in result:
                        if event.get("content"):
                            full_content += event["content"]
                    return {"response": full_content}
                else:
                    return {"response": str(result)}
            else:
                return {"error": f"Erro do servidor: {response.status_code} - {response.text}"}
                
        except requests.exceptions.Timeout:
            return {
                "error": "⏱️ **Timeout** - A resposta está demorando mais que o esperado. "
                        "Isso pode acontecer com análises complexas. "
                        "Tente novamente com uma pergunta mais específica."
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "🔌 **Conexão perdida** - Verifique se o backend está rodando na porta 7777."
            }
        except Exception as e:
            return {
                "error": f"❌ **Erro inesperado**: {str(e)}"
            }
            
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        return {"error": f"Erro de processamento: {str(e)}"}

def render_session_sidebar():
    """Renderiza sidebar de gerenciamento de sessões."""
    with st.sidebar:
        st.title("🧠 Agno Teams Pro")
        st.markdown("Sistema inteligente de agentes especializados")
        
        # Status do backend
        if check_backend_health():
            st.success("✅ Backend conectado")
        else:
            st.error("❌ Backend offline")
            st.warning("Execute o backend primeiro:")
            st.code("python agno_teams_playground.py")
            return False
        
        st.markdown("---")
        
        # Gerenciamento de sessões
        st.subheader("💬 Sessões")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("➕ Nova Sessão", use_container_width=True):
                create_new_session()
        
        with col2:
            if st.button("🔄", help="Atualizar lista"):
                st.cache_data.clear()
                st.rerun()
        
        # Busca de sessões
        search_query = st.text_input("🔍 Buscar sessões", placeholder="Digite para buscar...")
        
        # Lista de sessões
        if search_query:
            sessions = st.session_state.session_manager.search_sessions(search_query)
        else:
            sessions = st.session_state.session_manager.get_sessions(limit=20)
        
        if sessions:
            st.markdown("**Sessões Recentes:**")
            
            for session in sessions:
                is_current = session['id'] == st.session_state.current_session_id
                
                # Container para cada sessão
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        if st.button(
                            f"{'🟢' if is_current else '⚪'} {session['name'][:25]}...",
                            key=f"session_{session['id']}",
                            help=f"Criada: {session['created_at'][:16]}\nMensagens: {session['message_count']}",
                            use_container_width=True
                        ):
                            st.session_state.current_session_id = session['id']
                            load_session_messages(session['id'])
                            st.rerun()
                    
                    with col2:
                        if st.button("✏️", key=f"edit_{session['id']}", help="Renomear"):
                            st.session_state[f"editing_{session['id']}"] = True
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_{session['id']}", help="Deletar"):
                            st.session_state.session_manager.delete_session(session['id'])
                            if st.session_state.current_session_id == session['id']:
                                st.session_state.current_session_id = None
                                st.session_state.messages = []
                            st.rerun()
                    
                    # Campo de edição de nome
                    if st.session_state.get(f"editing_{session['id']}", False):
                        new_name = st.text_input(
                            "Novo nome:",
                            value=session['name'],
                            key=f"new_name_{session['id']}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Salvar", key=f"save_{session['id']}"):
                                st.session_state.session_manager.update_session(
                                    session['id'], name=new_name
                                )
                                st.session_state[f"editing_{session['id']}"] = False
                                st.rerun()
                        
                        with col2:
                            if st.button("❌ Cancelar", key=f"cancel_{session['id']}"):
                                st.session_state[f"editing_{session['id']}"] = False
                                st.rerun()
        else:
            st.info("Nenhuma sessão encontrada")
        
        # Informações da sessão atual
        if st.session_state.current_session_id:
            current_session = st.session_state.session_manager.get_session(
                st.session_state.current_session_id
            )
            if current_session:
                st.markdown("---")
                st.markdown("**Sessão Atual:**")
                st.info(f"📝 {current_session['name']}")
                st.caption(f"💬 {current_session['message_count']} mensagens")
                st.caption(f"🕒 {current_session['updated_at'][:16]}")
        
        return True

def render_team_selection():
    """Renderiza seleção de team."""
    st.subheader("🎯 Selecionar Team")
    teams = get_teams()
    
    if teams:
        team_options = []
        team_mapping = {}
        
        for team in teams:
            team_name = team.get("name", "Team sem nome")
            team_id = team.get("team_id", "")
            team_options.append(team_name)
            team_mapping[team_name] = team_id
        
        selected_team_name = st.selectbox(
            "Escolha um team:",
            ["Auto (Primeiro disponível)"] + team_options,
            index=0
        )
        
        if selected_team_name == "Auto (Primeiro disponível)":
            st.session_state.selected_team_id = teams[0].get("team_id") if teams else None
            st.info("🔄 Usando o primeiro team disponível")
        else:
            st.session_state.selected_team_id = team_mapping[selected_team_name]
            st.success(f"🎯 Team selecionado: {selected_team_name}")
        
        # Detalhes do team selecionado
        if st.session_state.selected_team_id:
            selected_team = next((t for t in teams if t.get("team_id") == st.session_state.selected_team_id), None)
            if selected_team:
                with st.expander("📋 Detalhes do Team"):
                    st.write(f"**ID**: {selected_team.get('team_id')}")
                    st.write(f"**Nome**: {selected_team.get('name')}")
                    if selected_team.get('description'):
                        st.write(f"**Descrição**: {selected_team.get('description')}")
                    if selected_team.get('members'):
                        st.write(f"**Membros**: {len(selected_team.get('members'))} agentes especialistas")
        
        return True
    else:
        st.warning("Nenhum team disponível")
        return False

def render_file_upload():
    """Renderiza seção de upload de arquivos melhorada."""
    st.subheader("📁 Upload de Dados")
    
    # Upload com drag & drop melhorado
    uploaded_file = st.file_uploader(
        "Arraste e solte um arquivo CSV para análise",
        type=['csv'],
        help="Faça upload de arquivos CSV para análise pelos especialistas em dados",
        key="file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            st.info(f"📤 Processando arquivo CSV: {uploaded_file.name}")
            
            # Processar CSV de forma otimizada
            file_bytes = uploaded_file.read()
            
            # Tentar diferentes encodings
            file_content = None
            for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    file_content = file_bytes.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if file_content is None:
                st.error("❌ Não foi possível ler o arquivo CSV. Verifique a codificação.")
                st.session_state.uploaded_file_data = None
                return
            
            # Análise básica do CSV
            lines = file_content.strip().split('\n')
            data_lines = lines[1:] if len(lines) > 1 else []
            
            # Tentar carregar com pandas para validação
            try:
                df = pd.read_csv(io.StringIO(file_content))
                
                st.success(f"✅ CSV carregado com sucesso!")
                
                # Informações do arquivo
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Linhas", len(df))
                with col2:
                    st.metric("📋 Colunas", len(df.columns))
                with col3:
                    st.metric("💾 Tamanho", f"{len(file_bytes)} bytes")
                
                # Preview dos dados
                with st.expander("👀 Preview dos Dados", expanded=True):
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Informações das colunas
                    st.markdown("**Informações das Colunas:**")
                    col_info = []
                    for col in df.columns:
                        dtype = str(df[col].dtype)
                        null_count = df[col].isnull().sum()
                        col_info.append({
                            "Coluna": col,
                            "Tipo": dtype,
                            "Nulos": null_count,
                            "% Nulos": f"{(null_count/len(df)*100):.1f}%"
                        })
                    
                    st.dataframe(pd.DataFrame(col_info), use_container_width=True)
                
                # Preparar dados para envio (limitar tamanho se necessário)
                if len(file_content) > 50000:  # 50KB
                    sample_lines = lines[:200]  # Primeiras 200 linhas
                    file_content = '\n'.join(sample_lines)
                    st.warning("⚠️ CSV muito grande. Usando amostra de 200 linhas para análise.")
                
                # Criar estrutura de dados
                upload_data = {
                    "content": file_content,
                    "filename": uploaded_file.name,
                    "type": "csv",
                    "size": len(file_bytes),
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist()
                }
                
                st.session_state.uploaded_file_data = json.dumps(upload_data)
                st.success("✅ Arquivo pronto para análise!")
                
            except Exception as e:
                st.error(f"❌ Erro ao processar CSV: {e}")
                st.session_state.uploaded_file_data = None
                
        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivo: {e}")
            st.session_state.uploaded_file_data = None
    else:
        st.session_state.uploaded_file_data = None
        
        # Instruções de uso
        st.markdown("""
        **💡 Como usar:**
        1. Arraste um arquivo CSV para a área acima
        2. O sistema fará uma análise prévia dos dados
        3. Faça perguntas sobre os dados na conversa
        4. Os agentes especialistas analisarão automaticamente
        
        **📊 Tipos de análise disponíveis:**
        - Análise estatística descritiva
        - Identificação de padrões e tendências
        - Detecção de outliers e anomalias
        - Análise de correlações
        - Visualizações e gráficos
        - Insights de negócio
        """)

def clean_message_content(content: str) -> str:
    """
    Limpa e formata o conteúdo da mensagem para exibição segura.
    Remove caracteres HTML problemáticos e formata adequadamente.
    """
    if not content:
        return ""
    
    # Escapar caracteres HTML
    safe_content = content.replace("<", "&lt;").replace(">", "&gt;")
    
    # Converter quebras de linha para HTML
    safe_content = safe_content.replace("\n", "<br>")
    
    # Processar markdown básico (negrito e itálico)
    import re
    safe_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', safe_content)
    safe_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', safe_content)
    
    return safe_content

def format_timestamp(timestamp: str) -> str:
    """Formata timestamp para exibição."""
    if not timestamp:
        return ""
    
    try:
        # Converter ISO timestamp para formato mais legível
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%d/%m %H:%M")
    except:
        # Fallback para primeiros 16 caracteres
        return timestamp[:16]

def render_chat_interface():
    """Renderiza interface de chat principal."""
    st.title("💬 Chat com Agentes Especializados")
    
    # Verificar timeout de processamento (evitar travamentos)
    if st.session_state.processing and st.session_state.last_processing_time:
        elapsed_time = time.time() - st.session_state.last_processing_time
        if elapsed_time > 300:  # 5 minutos de timeout
            st.session_state.processing = False
            st.session_state.last_processing_time = None
            st.warning("⏱️ Timeout de processamento atingido. Sistema resetado.")
    
    # Verificar se há sessão ativa
    if not st.session_state.current_session_id:
        st.info("👈 Selecione ou crie uma sessão na barra lateral para começar.")
        return
    
    # Container para mensagens
    chat_container = st.container()
    
    with chat_container:
        # Exibir mensagens
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 Você:</strong>
                    <div class="message-content">{clean_message_content(message["content"])}</div>
                    <div class="message-timestamp">{format_timestamp(message.get("timestamp", ""))}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 Assistente:</strong>
                    <div class="message-content">{clean_message_content(message["content"])}</div>
                    <div class="message-timestamp">{format_timestamp(message.get("timestamp", ""))}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Indicador de processamento
    if st.session_state.processing:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            <div class="loading-indicator">
                <div class="spinner"></div>
                <span>🤖 Agentes processando sua solicitação...</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🛑 Cancelar", type="secondary"):
                st.session_state.processing = False
                st.session_state.last_processing_time = None
                st.warning("Processamento cancelado pelo usuário.")
                st.rerun()
    
    # Input de mensagem
    st.markdown("---")
    
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_area(
                "Digite sua mensagem:",
                placeholder="Ex: Analise os dados do arquivo CSV que enviei...",
                height=100,
                key="user_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento
            submit_button = st.form_submit_button(
                "📤 Enviar",
                use_container_width=True,
                disabled=st.session_state.processing
            )
    
    # Processar mensagem
    if submit_button and user_input and not st.session_state.processing:
        if not st.session_state.selected_team_id:
            st.error("❌ Selecione um team antes de enviar mensagens.")
            return
        
        # Adicionar mensagem do usuário
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.messages.append(user_message)
        
        # Salvar mensagem na sessão
        st.session_state.session_manager.add_message(
            st.session_state.current_session_id,
            "user",
            user_input
        )
        
        # Marcar como processando e processar imediatamente
        st.session_state.processing = True
        st.session_state.last_processing_time = time.time()
        
        # Enviar para o team
        with st.spinner("🤖 Agentes processando..."):
            response = send_message_to_team(
                user_input,
                st.session_state.selected_team_id,
                st.session_state.uploaded_file_data
            )
        
        # Processar resposta
        if "error" in response:
            assistant_message = {
                "role": "assistant",
                "content": f"❌ {response['error']}",
                "timestamp": datetime.now().isoformat()
            }
        else:
            assistant_message = {
                "role": "assistant",
                "content": response["response"],
                "timestamp": datetime.now().isoformat()
            }
        
        st.session_state.messages.append(assistant_message)
        
        # Salvar resposta na sessão
        st.session_state.session_manager.add_message(
            st.session_state.current_session_id,
            "assistant",
            assistant_message["content"]
        )
        
        # Desmarcar processamento e atualizar interface
        st.session_state.processing = False
        st.session_state.last_processing_time = None
        st.rerun()

def render_examples():
    """Renderiza exemplos de perguntas."""
    with st.expander("💡 Exemplos de Perguntas", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📊 Análise de Dados (CSV)**
            - "Analise este dataset e me dê insights"
            - "Crie gráficos para visualizar os dados"
            - "Qual é a correlação entre as variáveis?"
            - "Identifique outliers nos dados"
            - "Faça uma análise estatística descritiva"
            """)
        
        with col2:
            st.markdown("""
            **💰 Análise Financeira**
            - "Como está o preço da ação PETR4?"
            - "Analise o mercado de criptomoedas"
            - "Calcule o ROI deste investimento"
            - "Compare ações do setor bancário"
            """)

def main():
    """Função principal da aplicação."""
    init_session_state()
    
    # Renderizar sidebar de sessões
    if not render_session_sidebar():
        return
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_chat_interface()
    
    with col2:
        render_team_selection()
        st.markdown("---")
        render_file_upload()
        st.markdown("---")
        render_examples()

if __name__ == "__main__":
    main()
