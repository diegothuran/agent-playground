"""
Session Manager - Gerenciamento avançado de sessões para o frontend Streamlit
"""

import json
import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import streamlit as st

class SessionManager:
    """Gerenciador de sessões com persistência em SQLite."""
    
    def __init__(self, db_path: str = "storage/sessions.db"):
        """Inicializa o gerenciador de sessões."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados de sessões."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    team_id TEXT,
                    message_count INTEGER DEFAULT 0,
                    metadata TEXT DEFAULT '{}'
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS session_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_messages_session_id 
                ON session_messages (session_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_updated_at 
                ON sessions (updated_at DESC)
            """)
    
    def create_session(self, name: str = None, team_id: str = None) -> str:
        """Cria uma nova sessão."""
        session_id = str(uuid.uuid4())
        
        if not name:
            name = f"Sessão {datetime.now().strftime('%d/%m %H:%M')}"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO sessions (id, name, team_id, metadata)
                VALUES (?, ?, ?, ?)
            """, (session_id, name, team_id, json.dumps({})))
        
        return session_id
    
    def get_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna lista de sessões ordenadas por data de atualização."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT id, name, created_at, updated_at, team_id, message_count, metadata
                FROM sessions 
                ORDER BY updated_at DESC 
                LIMIT ?
            """, (limit,))
            
            sessions = []
            for row in cursor:
                session = dict(row)
                session['metadata'] = json.loads(session['metadata'] or '{}')
                sessions.append(session)
            
            return sessions
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retorna dados de uma sessão específica."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT id, name, created_at, updated_at, team_id, message_count, metadata
                FROM sessions 
                WHERE id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            if row:
                session = dict(row)
                session['metadata'] = json.loads(session['metadata'] or '{}')
                return session
            
            return None
    
    def update_session(self, session_id: str, name: str = None, metadata: Dict = None):
        """Atualiza dados de uma sessão."""
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        
        if metadata:
            updates.append("metadata = ?")
            params.append(json.dumps(metadata))
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(session_id)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(f"""
                    UPDATE sessions 
                    SET {', '.join(updates)}
                    WHERE id = ?
                """, params)
    
    def delete_session(self, session_id: str):
        """Deleta uma sessão e todas suas mensagens."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Dict = None):
        """Adiciona uma mensagem à sessão."""
        with sqlite3.connect(self.db_path) as conn:
            # Adicionar mensagem
            conn.execute("""
                INSERT INTO session_messages (session_id, role, content, metadata)
                VALUES (?, ?, ?, ?)
            """, (session_id, role, content, json.dumps(metadata or {})))
            
            # Atualizar contador de mensagens e timestamp da sessão
            conn.execute("""
                UPDATE sessions 
                SET message_count = message_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (session_id,))
    
    def get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Retorna mensagens de uma sessão."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT role, content, timestamp, metadata
                FROM session_messages 
                WHERE session_id = ?
                ORDER BY timestamp ASC
            """, (session_id,))
            
            messages = []
            for row in cursor:
                message = dict(row)
                message['metadata'] = json.loads(message['metadata'] or '{}')
                messages.append(message)
            
            return messages
    
    def search_sessions(self, query: str) -> List[Dict[str, Any]]:
        """Busca sessões por nome ou conteúdo."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT DISTINCT s.id, s.name, s.created_at, s.updated_at, 
                       s.team_id, s.message_count, s.metadata
                FROM sessions s
                LEFT JOIN session_messages m ON s.id = m.session_id
                WHERE s.name LIKE ? OR m.content LIKE ?
                ORDER BY s.updated_at DESC
                LIMIT 20
            """, (f"%{query}%", f"%{query}%"))
            
            sessions = []
            for row in cursor:
                session = dict(row)
                session['metadata'] = json.loads(session['metadata'] or '{}')
                sessions.append(session)
            
            return sessions
    
    def cleanup_old_sessions(self, days: int = 30):
        """Remove sessões antigas."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM sessions 
                WHERE updated_at < ?
            """, (cutoff_date.isoformat(),))
            
            return cursor.rowcount
    
    def export_session(self, session_id: str) -> Dict[str, Any]:
        """Exporta uma sessão completa."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        messages = self.get_session_messages(session_id)
        
        return {
            "session": session,
            "messages": messages,
            "exported_at": datetime.now().isoformat()
        }
    
    def import_session(self, session_data: Dict[str, Any]) -> str:
        """Importa uma sessão."""
        # Criar nova sessão
        session_id = self.create_session(
            name=f"[Importada] {session_data['session']['name']}",
            team_id=session_data['session'].get('team_id')
        )
        
        # Importar mensagens
        for message in session_data['messages']:
            self.add_message(
                session_id=session_id,
                role=message['role'],
                content=message['content'],
                metadata=message.get('metadata', {})
            )
        
        return session_id

# Instância global do gerenciador
_session_manager = None

def get_session_manager() -> SessionManager:
    """Retorna instância singleton do gerenciador de sessões."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager

