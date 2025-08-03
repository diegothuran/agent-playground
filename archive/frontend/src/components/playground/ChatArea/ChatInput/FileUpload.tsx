import { useState, useRef, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import Icon from '@/components/ui/icon'
import { toast } from 'sonner'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  disabled?: boolean
}

const FileUpload = ({ onFileSelect, disabled }: FileUploadProps) => {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (!disabled) {
      setIsDragging(true)
    }
  }, [disabled])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    if (disabled) return

    const files = Array.from(e.dataTransfer.files)
    const file = files[0]

    if (file) {
      validateAndSelectFile(file)
    }
  }, [disabled])

  const validateAndSelectFile = (file: File) => {
    // Validar tipo de arquivo
    const allowedTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'text/plain',
      'application/json'
    ]
    
    const allowedExtensions = ['.csv', '.xlsx', '.xls', '.txt', '.json']
    const hasValidExtension = allowedExtensions.some(ext => 
      file.name.toLowerCase().endsWith(ext)
    )

    if (!allowedTypes.includes(file.type) && !hasValidExtension) {
      toast.error('Tipo de arquivo não suportado. Use CSV, Excel, TXT ou JSON.')
      return
    }

    // Validar tamanho (máximo 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('Arquivo muito grande. Máximo 10MB.')
      return
    }

    onFileSelect(file)
    toast.success(`Arquivo "${file.name}" selecionado!`)
  }

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      validateAndSelectFile(file)
    }
  }

  const handleButtonClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="relative">
      {/* Input hidden */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv,.xlsx,.xls,.txt,.json"
        onChange={handleFileInputChange}
        className="hidden"
        disabled={disabled}
      />

      {/* Botão de upload */}
      <Button
        onClick={handleButtonClick}
        disabled={disabled}
        size="icon"
        variant="outline"
        className="rounded-xl border-accent bg-transparent p-3 text-primary hover:bg-accent/10"
        title="Anexar arquivo (CSV, Excel, TXT, JSON)"
      >
        <Icon type="plus-icon" size="sm" />
      </Button>

      {/* Overlay de drag and drop */}
      {isDragging && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/20 backdrop-blur-sm"
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="rounded-lg border-2 border-dashed border-primary bg-background p-8 text-center">
            <Icon type="download" size="lg" className="mx-auto mb-4 text-primary" />
            <p className="text-lg font-medium text-primary">
              Solte o arquivo aqui
            </p>
            <p className="text-sm text-muted-foreground">
              CSV, Excel, TXT ou JSON (máx. 10MB)
            </p>
          </div>
        </div>
      )}

      {/* Zona de drop invisível */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className="absolute inset-0"
      />
    </div>
  )
}

export default FileUpload
