import { memo, useEffect, useState } from 'react'
import { cn } from '@/lib/utils'

interface ChartDisplayProps {
  content: string
  className?: string
}

/**
 * Componente para detectar e exibir gráficos em base64 nas mensagens
 */
const ChartDisplay = ({ content, className }: ChartDisplayProps) => {
  const [charts, setCharts] = useState<string[]>([])

  useEffect(() => {
    // Regex para detectar URLs de dados base64 de imagem
    const base64ImageRegex = /data:image\/[a-zA-Z]*;base64,([^)]*)/g
    const matches = content.match(base64ImageRegex)
    
    if (matches) {
      setCharts(matches)
    } else {
      setCharts([])
    }
  }, [content])

  if (charts.length === 0) {
    return null
  }

  return (
    <div
      className={cn(
        'grid max-w-4xl gap-4 mt-4',
        charts.length > 1 ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1'
      )}
    >
      {charts.map((chart, index) => (
        <div key={index} className="group relative">
          <div className="rounded-lg border bg-card p-2 shadow-sm">
            <img
              src={chart}
              alt={`Gráfico gerado ${index + 1}`}
              className="w-full h-auto rounded-md"
              onError={(e) => {
                const parent = e.currentTarget.parentElement?.parentElement
                if (parent) {
                  parent.innerHTML = `
                    <div class="flex h-40 flex-col items-center justify-center gap-2 rounded-md bg-secondary/50 text-muted">
                      <p class="text-destructive">Erro ao carregar gráfico</p>
                      <p class="text-xs text-muted-foreground">Gráfico ${index + 1}</p>
                    </div>
                  `
                }
              }}
            />
            <div className="mt-2 text-xs text-muted-foreground text-center">
              📊 Gráfico gerado automaticamente
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default memo(ChartDisplay)

ChartDisplay.displayName = 'ChartDisplay'
