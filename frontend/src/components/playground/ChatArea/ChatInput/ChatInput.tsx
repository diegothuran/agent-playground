'use client'
import { useState } from 'react'
import { toast } from 'sonner'
import { TextArea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { usePlaygroundStore } from '@/store'
import useAIChatStreamHandler from '@/hooks/useAIStreamHandler'
import { useQueryState } from 'nuqs'
import Icon from '@/components/ui/icon'
import DataInputModal from './DataInputModal'

const ChatInput = () => {
  const { chatInputRef } = usePlaygroundStore()

  const { handleStreamResponse } = useAIChatStreamHandler()
  const [selectedAgent] = useQueryState('agent')
  const [inputMessage, setInputMessage] = useState('')
  const isStreaming = usePlaygroundStore((state) => state.isStreaming)

  const handleSubmit = async () => {
    if (!inputMessage.trim()) return

    const currentMessage = inputMessage
    setInputMessage('')

    try {
      await handleStreamResponse(currentMessage)
    } catch (error) {
      toast.error(
        `Error in handleSubmit: ${
          error instanceof Error ? error.message : String(error)
        }`
      )
    }
  }

  const handleDataSubmit = async (data: string, source: 'file' | 'paste', fileName?: string) => {
    let messageToSend = ''
    
    if (source === 'file' && fileName) {
      const fileInfo = `📁 Arquivo: ${fileName}\n\n`
      messageToSend = `${fileInfo}Analise este arquivo de dados:\n\n${data}`
    } else {
      messageToSend = `Analise estes dados:\n\n${data}`
    }

    try {
      await handleStreamResponse(messageToSend)
    } catch (error) {
      toast.error(
        `Error in handleDataSubmit: ${
          error instanceof Error ? error.message : String(error)
        }`
      )
    }
  }

  return (
    <div className="relative mx-auto mb-1 w-full max-w-2xl font-geist">
      {/* Input principal */}
      <div className="flex items-end justify-center gap-x-2">
        <TextArea
          placeholder="Pergunte qualquer coisa..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => {
            if (
              e.key === 'Enter' &&
              !e.nativeEvent.isComposing &&
              !e.shiftKey &&
              !isStreaming
            ) {
              e.preventDefault()
              handleSubmit()
            }
          }}
          className="w-full border border-accent bg-primaryAccent px-4 text-sm text-primary focus:border-accent"
          disabled={!selectedAgent}
          ref={chatInputRef}
        />
        
        {/* Modal de análise de dados */}
        <DataInputModal 
          onDataSubmit={handleDataSubmit}
          disabled={!selectedAgent || isStreaming}
        />

        {/* Botão de envio */}
        <Button
          onClick={handleSubmit}
          disabled={!selectedAgent || !inputMessage.trim() || isStreaming}
          size="icon"
          className="rounded-xl bg-primary p-5 text-primaryAccent"
        >
          <Icon type="send" color="primaryAccent" />
        </Button>
      </div>
    </div>
  )
}

export default ChatInput
