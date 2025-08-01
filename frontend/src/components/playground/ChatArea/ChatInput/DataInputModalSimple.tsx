'use client'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { TextArea } from '@/components/ui/textarea'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import Icon from '@/components/ui/icon'
import FileUpload from './FileUpload'
import { toast } from 'sonner'

interface DataInputModalProps {
  onDataSubmit: (data: string, source: 'file' | 'paste', fileName?: string) => void
  disabled?: boolean
}

const DataInputModal = ({ onDataSubmit, disabled }: DataInputModalProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const [pastedData, setPastedData] = useState('')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [activeTab, setActiveTab] = useState<'paste' | 'file'>('paste')

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    setActiveTab('file')
  }

  const readFileContent = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        const content = e.target?.result as string
        resolve(content)
      }
      reader.onerror = reject
      reader.readAsText(file)
    })
  }

  const handleSubmit = async () => {
    if (activeTab === 'paste' && pastedData.trim()) {
      onDataSubmit(pastedData.trim(), 'paste')
      setPastedData('')
      setIsOpen(false)
      toast.success('Dados enviados para análise!')
    } else if (activeTab === 'file' && selectedFile) {
      try {
        const content = await readFileContent(selectedFile)
        onDataSubmit(content, 'file', selectedFile.name)
        setSelectedFile(null)
        setIsOpen(false)
        toast.success(`Arquivo "${selectedFile.name}" enviado para análise!`)
      } catch (error) {
        toast.error('Erro ao ler o arquivo')
      }
    }
  }

  const handleClose = () => {
    setIsOpen(false)
    setPastedData('')
    setSelectedFile(null)
  }

  const isValidData = () => {
    if (activeTab === 'paste') {
      return pastedData.trim().length > 0
    }
    return selectedFile !== null
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button
          disabled={disabled}
          size="icon"
          variant="outline"
          className="rounded-xl border-accent bg-transparent p-3 text-primary hover:bg-accent/10"
          title="Analisar dados (Upload ou Copy/Paste)"
        >
          <Icon type="sheet" size="sm" />
        </Button>
      </DialogTrigger>
      
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Icon type="sheet" size="sm" />
            Analisar Dados
          </DialogTitle>
        </DialogHeader>

        {/* Navegação simples */}
        <div className="flex gap-2 mb-4">
          <Button
            variant={activeTab === 'paste' ? 'default' : 'outline'}
            onClick={() => setActiveTab('paste')}
            className="flex items-center gap-2"
          >
            <Icon type="edit" size="xs" />
            Copy & Paste
          </Button>
          <Button
            variant={activeTab === 'file' ? 'default' : 'outline'}
            onClick={() => setActiveTab('file')}
            className="flex items-center gap-2"
          >
            <Icon type="plus-icon" size="xs" />
            Upload Arquivo
          </Button>
        </div>

        {/* Conteúdo das abas */}
        {activeTab === 'paste' && (
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">
                Cole seus dados CSV, JSON ou texto:
              </label>
              <TextArea
                placeholder={`Cole aqui os dados para análise. Exemplos:

CSV:
Nome,Idade,Cidade
João,30,São Paulo
Maria,25,Rio de Janeiro

JSON:
[{"nome": "João", "idade": 30, "cidade": "São Paulo"}]

Ou qualquer outro formato de dados...`}
                value={pastedData}
                onChange={(e) => setPastedData(e.target.value)}
                className="min-h-[200px] font-mono text-sm"
              />
              <p className="text-xs text-muted-foreground">
                Suporte para CSV, JSON, TSV e outros formatos de dados estruturados
              </p>
            </div>
          </div>
        )}

        {activeTab === 'file' && (
          <div className="space-y-4">
            {!selectedFile ? (
              <div className="border-2 border-dashed border-accent rounded-lg p-8 text-center">
                <Icon type="download" size="lg" className="mx-auto mb-4 text-muted-foreground" />
                <p className="text-lg font-medium mb-2">Selecione um arquivo</p>
                <p className="text-sm text-muted-foreground mb-4">
                  Arraste e solte ou clique para selecionar
                </p>
                <FileUpload 
                  onFileSelect={handleFileSelect}
                  disabled={disabled}
                />
                <p className="text-xs text-muted-foreground mt-2">
                  Suporte: CSV, Excel (.xlsx, .xls), TXT, JSON (máx. 10MB)
                </p>
              </div>
            ) : (
              <div className="flex items-center gap-3 rounded-lg border border-accent bg-accent/10 p-4">
                <Icon type="sheet" className="text-primary" />
                <div className="flex-1">
                  <p className="font-medium text-primary">{selectedFile.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(selectedFile.size / 1024).toFixed(1)}KB
                  </p>
                </div>
                <Button
                  onClick={() => setSelectedFile(null)}
                  size="icon"
                  variant="ghost"
                  className="h-8 w-8"
                >
                  <Icon type="x" size="xs" />
                </Button>
              </div>
            )}
          </div>
        )}

        <div className="flex justify-end gap-2 pt-4">
          <Button
            onClick={handleClose}
            variant="outline"
          >
            Cancelar
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!isValidData()}
            className="bg-primary text-primaryAccent"
          >
            <Icon type="send" size="xs" className="mr-2" />
            Analisar Dados
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}

export default DataInputModal
