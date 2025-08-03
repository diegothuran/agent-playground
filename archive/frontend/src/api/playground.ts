import { toast } from 'sonner'

import { APIRoutes } from './routes'

import { Agent, ComboboxAgent, SessionEntry } from '@/types/playground'

export const getPlaygroundAgentsOrTeamsAPI = async (
  endpoint: string
): Promise<{ agents: ComboboxAgent[], type: 'agents' | 'teams' }> => {
  // Primeiro tenta buscar agents
  try {
    const agentsUrl = APIRoutes.GetPlaygroundAgents(endpoint)
    const agentsResponse = await fetch(agentsUrl, { method: 'GET' })
    
    if (agentsResponse.ok) {
      const agentsData = await agentsResponse.json()
      if (agentsData && agentsData.length > 0) {
        const agents: ComboboxAgent[] = agentsData.map((item: Agent) => ({
          value: item.agent_id || '',
          label: item.name || '',
          model: item.model || '',
          storage: item.storage || false
        }))
        return { agents, type: 'agents' }
      }
    }
  } catch (error) {
    console.log('No agents found, trying teams...')
  }

  // Se não encontrou agents, tenta buscar teams
  try {
    const teamsUrl = APIRoutes.GetPlaygroundTeams(endpoint)
    const teamsResponse = await fetch(teamsUrl, { method: 'GET' })
    
    if (teamsResponse.ok) {
      const teamsData = await teamsResponse.json()
      if (teamsData && teamsData.length > 0) {
        const teams: ComboboxAgent[] = teamsData.map((item: any) => ({
          value: item.team_id || item.id || '',
          label: item.name || '',
          model: item.model || '',
          storage: item.storage || false
        }))
        return { agents: teams, type: 'teams' }
      }
    }
  } catch (error) {
    console.log('No teams found either')
  }

  toast.error('No agents or teams found in the playground')
  return { agents: [], type: 'agents' }
}

// Mantém a função original para compatibilidade
export const getPlaygroundAgentsAPI = async (
  endpoint: string
): Promise<ComboboxAgent[]> => {
  const result = await getPlaygroundAgentsOrTeamsAPI(endpoint)
  return result.agents
}

export const getPlaygroundStatusAPI = async (base: string): Promise<number> => {
  const response = await fetch(APIRoutes.PlaygroundStatus(base), {
    method: 'GET'
  })
  return response.status
}

export const getAllPlaygroundSessionsAPI = async (
  base: string,
  agentId: string
): Promise<SessionEntry[]> => {
  try {
    const response = await fetch(
      APIRoutes.GetPlaygroundSessions(base, agentId),
      {
        method: 'GET'
      }
    )
    if (!response.ok) {
      if (response.status === 404) {
        // Return empty array when storage is not enabled
        return []
      }
      throw new Error(`Failed to fetch sessions: ${response.statusText}`)
    }
    return response.json()
  } catch {
    return []
  }
}

export const getPlaygroundSessionAPI = async (
  base: string,
  agentId: string,
  sessionId: string
) => {
  const response = await fetch(
    APIRoutes.GetPlaygroundSession(base, agentId, sessionId),
    {
      method: 'GET'
    }
  )
  return response.json()
}

export const deletePlaygroundSessionAPI = async (
  base: string,
  agentId: string,
  sessionId: string
) => {
  const response = await fetch(
    APIRoutes.DeletePlaygroundSession(base, agentId, sessionId),
    {
      method: 'DELETE'
    }
  )
  return response
}
