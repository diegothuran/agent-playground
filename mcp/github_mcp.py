"""
Exemplo de MCP especializado para GitHub API
"""
import requests
import json
from typing import Dict, Any, List, Optional
from mcp.mcp_tools import MCPTools


class GitHubMCPTools(MCPTools):
    """Ferramentas MCP especializadas para GitHub API."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__()
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Agno-Playground-MCP"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def search_repositories(self, query: str, sort: str = "stars", per_page: int = 10) -> dict:
        """Busca repositórios no GitHub."""
        try:
            params = {
                "q": query,
                "sort": sort,
                "per_page": min(per_page, 100)  # GitHub API limit
            }
            
            response = requests.get(
                f"{self.base_url}/search/repositories",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                repos = []
                for repo in data.get("items", []):
                    repos.append({
                        "name": repo["full_name"],
                        "description": repo.get("description", ""),
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"],
                        "language": repo.get("language", ""),
                        "url": repo["html_url"]
                    })
                
                return {
                    "status": "success",
                    "total_count": data.get("total_count", 0),
                    "repositories": repos
                }
            else:
                return {
                    "status": "error",
                    "message": f"GitHub API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao buscar repositórios: {str(e)}"
            }
    
    def get_repository_info(self, owner: str, repo: str) -> dict:
        """Obtém informações detalhadas de um repositório."""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "repository": {
                        "name": data["full_name"],
                        "description": data.get("description", ""),
                        "stars": data["stargazers_count"],
                        "forks": data["forks_count"],
                        "watchers": data["watchers_count"],
                        "language": data.get("language", ""),
                        "topics": data.get("topics", []),
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"],
                        "clone_url": data["clone_url"],
                        "html_url": data["html_url"],
                        "default_branch": data["default_branch"]
                    }
                }
            elif response.status_code == 404:
                return {
                    "status": "error",
                    "message": f"Repositório {owner}/{repo} não encontrado"
                }
            else:
                return {
                    "status": "error",
                    "message": f"GitHub API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao obter info do repositório: {str(e)}"
            }
    
    def get_repository_issues(self, owner: str, repo: str, state: str = "open", per_page: int = 10) -> dict:
        """Lista issues de um repositório."""
        try:
            params = {
                "state": state,
                "per_page": min(per_page, 100)
            }
            
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/issues",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = []
                for issue in data:
                    # Pular pull requests (eles aparecem como issues na API)
                    if "pull_request" not in issue:
                        issues.append({
                            "number": issue["number"],
                            "title": issue["title"],
                            "state": issue["state"],
                            "created_at": issue["created_at"],
                            "updated_at": issue["updated_at"],
                            "author": issue["user"]["login"],
                            "labels": [label["name"] for label in issue.get("labels", [])],
                            "url": issue["html_url"]
                        })
                
                return {
                    "status": "success",
                    "issues": issues,
                    "count": len(issues)
                }
            else:
                return {
                    "status": "error",
                    "message": f"GitHub API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao listar issues: {str(e)}"
            }
    
    def get_user_info(self, username: str) -> dict:
        """Obtém informações de um usuário GitHub."""
        try:
            response = requests.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "user": {
                        "login": data["login"],
                        "name": data.get("name", ""),
                        "bio": data.get("bio", ""),
                        "company": data.get("company", ""),
                        "location": data.get("location", ""),
                        "email": data.get("email", ""),
                        "blog": data.get("blog", ""),
                        "public_repos": data["public_repos"],
                        "followers": data["followers"],
                        "following": data["following"],
                        "created_at": data["created_at"],
                        "avatar_url": data["avatar_url"],
                        "html_url": data["html_url"]
                    }
                }
            elif response.status_code == 404:
                return {
                    "status": "error",
                    "message": f"Usuário {username} não encontrado"
                }
            else:
                return {
                    "status": "error",
                    "message": f"GitHub API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao obter info do usuário: {str(e)}"
            }
