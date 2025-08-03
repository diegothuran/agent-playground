#!/usr/bin/env python3
"""
🚀 Agno Teams - Frontend Streamlit

Interface web simples que consome o playground backend existente.
Usa os endpoints corretos do Agno Playground.

Uso:
streamlit run streamlit_frontend.py
"""

import streamlit as st
import requests
import json
import pandas as pd
import numpy as np  # Adicionar import explícito do numpy
import io
import time
from typing import Optional, Dict, Any, List
import logging

# Configuração da página
st.set_page_config(
    page_title="🧠 Agno Teams",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações
BACKEND_URL = "http://localhost:7777"

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_session_state():
    """Inicializa estado da sessão"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_file_data" not in st.session_state:
        st.session_state.uploaded_file_data = None
    if "selected_team_id" not in st.session_state:
        st.session_state.selected_team_id = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = None

def check_backend_health():
    """Verifica se o backend está rodando usando endpoint correto"""
    try:
        response = requests.get(f"{BACKEND_URL}/v1/playground/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_teams():
    """Busca lista de teams disponíveis"""
    try:
        response = requests.get(f"{BACKEND_URL}/v1/playground/teams", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Erro ao buscar teams: {e}")
        return []

def send_message_to_team(message: str, team_id: str, file_content: Optional[str] = None):
    """Envia mensagem para um team específico"""
    try:
        enhanced_message = message
        
        # Se há arquivo anexado, processar conforme o tipo
        if file_content:
            try:
                import json
                # Tentar carregar como JSON estruturado (novos uploads)
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
                # Fallback para uploads antigos (texto simples)
                enhanced_message = f"{message}\n\nArquivo CSV carregado para análise:\n```csv\n{file_content[:2000]}...\n```"
        
        # Preparar dados da execução usando multipart/form-data (formato correto da API)
        files = {
            'message': (None, enhanced_message),
            'stream': (None, 'false')  # Desabilitar streaming para interface mais simples
        }
        
        # Enviar para o team específico usando endpoint correto
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/playground/teams/{team_id}/runs",
                files=files,
                timeout=180  # Aumentado para 3 minutos
            )
            
            if response.status_code == 200:
                result = response.json()
                # Verificar se é um evento completo ou lista de eventos
                if isinstance(result, dict):
                    # Evento único - extrair conteúdo
                    content = result.get("content", str(result))
                    return {"response": content}
                elif isinstance(result, list):
                    # Lista de eventos - concatenar conteúdos
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
                        "Tente novamente com uma pergunta mais específica ou aguarde um momento."
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

def render_sidebar():
    """Renderiza sidebar com informações e upload"""
    with st.sidebar:
        st.title("🧠 Agno Teams")
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
        
        # Seleção de team
        st.subheader("🎯 Selecionar Team")
        teams = get_teams()
        
        if teams:
            # Criar lista de opções para o selectbox
            team_options = []
            team_mapping = {}
            
            for team in teams:
                team_name = team.get("name", "Team sem nome")
                team_id = team.get("team_id", "")  # Usar 'team_id' em vez de 'id'
                team_options.append(team_name)
                team_mapping[team_name] = team_id
            
            # Selectbox para escolher team
            selected_team_name = st.selectbox(
                "Escolha um team:",
                ["Auto (Primeiro disponível)"] + team_options,
                index=0
            )
            
            if selected_team_name == "Auto (Primeiro disponível)":
                st.session_state.selected_team_id = teams[0].get("team_id") if teams else None  # Usar 'team_id'
                st.info("🔄 Usando o primeiro team disponível")
            else:
                st.session_state.selected_team_id = team_mapping[selected_team_name]
                st.info(f"🎯 Team selecionado: {selected_team_name}")
            
            # Mostrar detalhes do team selecionado
            if st.session_state.selected_team_id:
                selected_team = next((t for t in teams if t.get("team_id") == st.session_state.selected_team_id), None)  # Usar 'team_id'
                if selected_team:
                    with st.expander("📋 Detalhes do Team"):
                        st.write(f"**ID**: {selected_team.get('team_id')}")  # Usar 'team_id'
                        st.write(f"**Nome**: {selected_team.get('name')}")
                        if selected_team.get('description'):
                            st.write(f"**Descrição**: {selected_team.get('description')}")
                        # Mostrar número de membros se disponível
                        if selected_team.get('members'):
                            st.write(f"**Membros**: {len(selected_team.get('members'))} agentes especialistas")
        else:
            st.warning("Nenhum team disponível")
            return False
        
        st.markdown("---")
        
        # Upload de arquivo
        st.subheader("📁 Upload de Dados")
        uploaded_file = st.file_uploader(
            "Arraste e solte um arquivo para análise",
            type=['csv', 'pdf', 'xls', 'xlsx'],
            help="Faça upload de CSV, PDF, Excel (XLS/XLSX) para análise pelos especialistas"
        )
        
        if uploaded_file is not None:
            try:
                # Detectar tipo de arquivo
                file_extension = uploaded_file.name.lower().split('.')[-1]
                st.info(f"📤 Processando arquivo {file_extension.upper()}...")
                
                file_content = None
                
                if file_extension == 'csv':
                    # Processar CSV (método ultra-simples)
                    file_bytes = uploaded_file.read()
                    
                    # Tentar decodificar
                    for encoding in ['utf-8', 'latin-1', 'cp1252']:
                        try:
                            file_content = file_bytes.decode(encoding)
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if file_content is None:
                        st.error("❌ Não foi possível ler o arquivo CSV")
                        st.session_state.uploaded_file_data = None
                        return True
                    
                    # Contar linhas básico
                    lines = file_content.strip().split('\n')
                    data_lines = lines[1:] if len(lines) > 1 else []
                    
                    st.success(f"✅ CSV carregado: {uploaded_file.name}")
                    st.info(f"📊 {len(data_lines)} linhas de dados")
                
                elif file_extension == 'pdf':
                    # Processar PDF - enviar como base64 para o backend
                    import base64
                    
                    file_bytes = uploaded_file.read()
                    file_content = base64.b64encode(file_bytes).decode('utf-8')
                    
                    st.success(f"✅ PDF carregado: {uploaded_file.name}")
                    st.info(f"� {len(file_bytes)} bytes - PDF será extraído pelo backend")
                    
                elif file_extension in ['xls', 'xlsx']:
                    # Processar Excel - enviar como base64 para o backend
                    import base64
                    
                    file_bytes = uploaded_file.read()
                    file_content = base64.b64encode(file_bytes).decode('utf-8')
                    
                    st.success(f"✅ Excel carregado: {uploaded_file.name}")
                    st.info(f"📊 {len(file_bytes)} bytes - Excel será processado pelo backend")
                
                else:
                    st.error("❌ Formato de arquivo não suportado")
                    st.session_state.uploaded_file_data = None
                    return True
                
                # Preview básico
                with st.expander("👀 Informações do arquivo"):
                    st.write(f"**Nome**: {uploaded_file.name}")
                    st.write(f"**Tipo**: {file_extension.upper()}")
                    st.write(f"**Tamanho**: {uploaded_file.size} bytes")
                    
                    if file_extension == 'csv' and file_content:
                        # Preview para CSV
                        lines = file_content.strip().split('\n')
                        st.text("Primeiras linhas do CSV:")
                        for i, line in enumerate(lines[:6]):
                            st.text(f"L{i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
                    
                    elif file_extension == 'pdf':
                        st.info("📄 PDF será extraído e analisado pelos agentes")
                        st.text("Conteúdo: Texto será extraído automaticamente")
                    
                    elif file_extension in ['xls', 'xlsx']:
                        st.info("📊 Planilha será processada pelos agentes de dados")
                        st.text("Conteúdo: Tabelas e dados serão extraídos automaticamente")
                
                # Preparar dados para envio
                if file_content:
                    # Limitar tamanho se muito grande (especialmente para CSV)
                    if file_extension == 'csv' and len(file_content) > 30000:
                        lines = file_content.strip().split('\n')
                        sample_lines = lines[:100]
                        file_content = '\n'.join(sample_lines)
                        st.warning("⚠️ CSV muito grande. Usando amostra de 100 linhas.")
                    
                    # Criar estrutura de dados com tipo de arquivo
                    upload_data = {
                        "content": file_content,
                        "filename": uploaded_file.name,
                        "type": file_extension,
                        "size": uploaded_file.size
                    }
                    
                    # Converter para string JSON para compatibilidade
                    import json
                    st.session_state.uploaded_file_data = json.dumps(upload_data)
                    st.success("✅ Arquivo pronto para análise!")
                
            except Exception as e:
                st.error(f"❌ Erro ao processar {file_extension.upper()}: {e}")
                st.session_state.uploaded_file_data = None
        else:
            st.session_state.uploaded_file_data = None
        
        st.markdown("---")
        
        # Exemplos de perguntas
        st.subheader("💡 Exemplos de Perguntas")
        with st.expander("📊 Análise de Dados (CSV/Excel)"):
            st.markdown("""
            - "Analise este dataset e me dê insights"
            - "Crie gráficos para visualizar os dados"
            - "Qual é a correlação entre as variáveis?"
            - "Identifique outliers nos dados"
            - "Processe esta planilha Excel"
            - "Compare dados entre abas da planilha"
            """)
        
        with st.expander("� Análise de Documentos (PDF)"):
            st.markdown("""
            - "Extraia as informações principais deste PDF"
            - "Faça um resumo do documento"
            - "Identifique dados e métricas no texto"
            - "Analise contratos e documentos legais"
            - "Extraia tabelas e dados estruturados"
            """)
        
        with st.expander("�💰 Análise Financeira"):
            st.markdown("""
            - "Como está o preço da ação PETR4?"
            - "Analise o mercado de criptomoedas"
            - "Compare IBOVESPA com S&P 500"
            - "Tendências do mercado financeiro"
            """)
        
        with st.expander("🌐 Pesquisa Web"):
            st.markdown("""
            - "Pesquise sobre inteligência artificial"
            - "Últimas notícias sobre tecnologia"
            - "Informações sobre empresa X"
            """)
        
        with st.expander("💻 Análise de Código"):
            st.markdown("""
            - "Revise este código Python"
            - "Como melhorar a performance?"
            - "Identifique bugs no código"
            """)
        
        with st.expander("📋 Tipos de Arquivo Suportados"):
            st.markdown("""
            - **📊 CSV**: Dados tabulares para análise estatística
            - **📄 PDF**: Documentos para extração de texto e dados
            - **📈 Excel (XLS/XLSX)**: Planilhas com múltiplas abas
            - **Tamanho máximo**: 30KB para CSV, sem limite para PDF/Excel
            """)
        
        return True

def render_chat():
    """Renderiza área de chat principal"""
    st.title("💬 Chat com Agno Teams")
    
    # Verificar se tem team selecionado
    if not st.session_state.selected_team_id:
        st.error("⚠️ Nenhum team selecionado. Configure na sidebar.")
        return
    
    # Container para mensagens
    chat_container = st.container()
    
    with chat_container:
        # Exibe mensagens do histórico
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                    # Mostra indicação se arquivo foi anexado
                    if message.get("has_file"):
                        file_type = message.get("file_type", "arquivo")
                        if file_type == "csv":
                            st.caption("📊 CSV anexado")
                        elif file_type == "pdf":
                            st.caption("� PDF anexado")
                        elif file_type in ["xls", "xlsx"]:
                            st.caption("📈 Excel anexado")
                        else:
                            st.caption("�📎 Arquivo anexado")
                else:
                    # Mensagem do assistente
                    content = message["content"]
                    
                    # Se a resposta contém código, exibir em bloco de código
                    if "```" in content:
                        st.markdown(content)
                    else:
                        st.write(content)
    
    # Input de mensagem
    if prompt := st.chat_input("Digite sua mensagem para os agentes..."):
        # Detectar tipo de arquivo anexado
        file_type = None
        if st.session_state.uploaded_file_data:
            try:
                import json
                file_data = json.loads(st.session_state.uploaded_file_data)
                file_type = file_data.get('type', 'arquivo')
            except:
                file_type = 'csv'  # Fallback para uploads antigos
        
        # Adiciona mensagem do usuário
        user_message = {
            "role": "user", 
            "content": prompt,
            "has_file": st.session_state.uploaded_file_data is not None,
            "file_type": file_type
        }
        st.session_state.messages.append(user_message)
        
        # Exibe mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
            if st.session_state.uploaded_file_data:
                if file_type == "csv":
                    st.caption("📊 CSV anexado")
                elif file_type == "pdf":
                    st.caption("📄 PDF anexado")
                elif file_type in ["xls", "xlsx"]:
                    st.caption("📈 Excel anexado")
                else:
                    st.caption("📎 Arquivo anexado")
        
        # Processa resposta do backend
        with st.chat_message("assistant"):
            with st.spinner("🤔 Os agentes estão analisando..."):
                # Envia para o team selecionado
                response = send_message_to_team(
                    message=prompt,
                    team_id=st.session_state.selected_team_id,
                    file_content=st.session_state.uploaded_file_data
                )
                
                if "error" in response:
                    st.error(f"❌ {response['error']}")
                    content = f"Erro: {response['error']}"
                else:
                    # Processa resposta bem-sucedida
                    content = response.get("response", response.get("message", "Resposta processada"))
                    
                    # Exibe resposta
                    if "```" in content:
                        st.markdown(content)
                    else:
                        st.write(content)
        
        # Salva resposta no histórico
        st.session_state.messages.append({
            "role": "assistant", 
            "content": content
        })

def main():
    """Função principal"""
    init_session_state()
    
    # Renderiza sidebar e verifica backend
    if render_sidebar():
        # Só renderiza o chat se o backend estiver online e team selecionado
        render_chat()
    else:
        # Backend offline - mostra instruções
        st.error("🚫 Backend não está rodando")
        st.markdown("""
        ### Como iniciar o sistema:
        
        1. **Em um terminal**, execute o backend:
        ```bash
        cd /home/diego/Documentos/RA/play
        python agno_teams_playground.py
        ```
        
        2. **Em outro terminal**, execute este frontend:
        ```bash
        streamlit run streamlit_frontend.py
        ```
        
        3. **Acesse**: http://localhost:8501
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
            🧠 Agno Teams Frontend - Powered by 
            <a href='https://docs.agno.com' target='_blank'>Agno Framework</a> + 
            <a href='https://streamlit.io' target='_blank'>Streamlit</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
