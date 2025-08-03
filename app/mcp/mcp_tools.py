import requests
import json
from typing import Dict, Any, List
import datetime

class MCPTools:
    """Ferramentas para conectar com serviços Model Context Protocol."""
    
    def __init__(self):
        self.name = "mcp_tools"
        self.mcp_servers = {}
    
    def register_mcp_server(self, name: str, url: str, port: int = 8888) -> dict:
        """Registra um servidor MCP."""
        try:
            server_url = f"http://{url}:{port}"
            self.mcp_servers[name] = server_url
            
            # Testa a conexão
            response = requests.get(f"{server_url}/health", timeout=5)
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": f"Servidor MCP '{name}' registrado com sucesso",
                    "url": server_url
                }
            else:
                return {
                    "status": "warning",
                    "message": f"Servidor registrado mas não está respondendo: {response.status_code}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao registrar servidor MCP: {str(e)}"
            }
    
    def list_mcp_servers(self) -> dict:
        """Lista todos os servidores MCP registrados."""
        return {
            "servers": list(self.mcp_servers.keys()),
            "count": len(self.mcp_servers)
        }
    
    def call_mcp_service(self, server_name: str, endpoint: str, data: Dict[str, Any] = None) -> dict:
        """Faz uma chamada para um serviço MCP."""
        try:
            if server_name not in self.mcp_servers:
                return {
                    "status": "error",
                    "message": f"Servidor '{server_name}' não encontrado"
                }
            
            server_url = self.mcp_servers[server_name]
            url = f"{server_url}/{endpoint.lstrip('/')}"
            
            if data:
                response = requests.post(url, json=data, timeout=10)
            else:
                response = requests.get(url, timeout=10)
            
            return {
                "status": "success",
                "status_code": response.status_code,
                "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro na chamada MCP: {str(e)}"
            }
    
    def check_mcp_health(self, server_name: str = None) -> dict:
        """Verifica a saúde dos servidores MCP."""
        try:
            if server_name:
                servers_to_check = {server_name: self.mcp_servers.get(server_name)}
            else:
                servers_to_check = self.mcp_servers
            
            health_status = {}
            
            for name, url in servers_to_check.items():
                if url is None:
                    health_status[name] = {"status": "not_found"}
                    continue
                
                try:
                    response = requests.get(f"{url}/health", timeout=5)
                    health_status[name] = {
                        "status": "healthy" if response.status_code == 200 else "unhealthy",
                        "response_time": response.elapsed.total_seconds(),
                        "status_code": response.status_code
                    }
                except Exception as e:
                    health_status[name] = {
                        "status": "error",
                        "error": str(e)
                    }
            
            return {
                "health_check": health_status,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro no health check: {str(e)}"
            }
