import { useCallback } from 'react'
import { toast } from 'sonner'

import { usePlaygroundStore } from '../store'

import { ComboboxAgent, type PlaygroundChatMessage } from '@/types/playground'
import {
  getPlaygroundAgentsOrTeamsAPI,
  getPlaygroundStatusAPI
} from '@/api/playground'
import { useQueryState } from 'nuqs'

const useChatActions = () => {
  const { chatInputRef } = usePlaygroundStore()
  const selectedEndpoint = usePlaygroundStore((state) => state.selectedEndpoint)
  const [, setSessionId] = useQueryState('session')
  const setMessages = usePlaygroundStore((state) => state.setMessages)
  const setIsEndpointActive = usePlaygroundStore(
    (state) => state.setIsEndpointActive
  )
  const setIsEndpointLoading = usePlaygroundStore(
    (state) => state.setIsEndpointLoading
  )
  const setAgents = usePlaygroundStore((state) => state.setAgents)
  const setSelectedModel = usePlaygroundStore((state) => state.setSelectedModel)
  const setPlaygroundType = usePlaygroundStore((state) => state.setPlaygroundType)
  const [agentId, setAgentId] = useQueryState('agent')

  const getStatus = useCallback(async () => {
    try {
      const status = await getPlaygroundStatusAPI(selectedEndpoint)
      return status
    } catch {
      return 503
    }
  }, [selectedEndpoint])

  const getAgentsOrTeams = useCallback(async () => {
    try {
      const result = await getPlaygroundAgentsOrTeamsAPI(selectedEndpoint)
      // Salva o tipo detectado no store para uso futuro
      setPlaygroundType(result.type)
      return result.agents
    } catch {
      toast.error('Error fetching agents or teams')
      return []
    }
  }, [selectedEndpoint, setPlaygroundType])

  const clearChat = useCallback(() => {
    setMessages([])
    setSessionId(null)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const focusChatInput = useCallback(() => {
    setTimeout(() => {
      requestAnimationFrame(() => chatInputRef?.current?.focus())
    }, 0)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const addMessage = useCallback(
    (message: PlaygroundChatMessage) => {
      setMessages((prevMessages) => [...prevMessages, message])
    },
    [setMessages]
  )

  const initializePlayground = useCallback(async () => {
    setIsEndpointLoading(true)
    try {
      const status = await getStatus()
      let agents: ComboboxAgent[] = []
      if (status === 200) {
        setIsEndpointActive(true)
        agents = await getAgentsOrTeams()
        // Sempre seleciona automaticamente o primeiro agente/team
        if (agents.length > 0) {
          const firstAgent = agents[0]
          setAgentId(firstAgent.value)
          setSelectedModel(firstAgent.model.provider || '')
          
          // Log para debug
          const playgroundType = usePlaygroundStore.getState().playgroundType
          console.log(`🎯 Detectado: ${playgroundType} - Selecionado: ${firstAgent.label}`)
        }
      } else {
        setIsEndpointActive(false)
      }
      setAgents(agents)
      return agents
    } catch {
      setIsEndpointLoading(false)
    } finally {
      setIsEndpointLoading(false)
    }
  }, [
    getStatus,
    getAgentsOrTeams,
    setIsEndpointActive,
    setIsEndpointLoading,
    setAgents,
    setAgentId,
    setSelectedModel,
    agentId
  ])

  return {
    clearChat,
    addMessage,
    getAgentsOrTeams,
    focusChatInput,
    initializePlayground
  }
}

export default useChatActions
