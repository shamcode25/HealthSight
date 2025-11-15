import { Chip, ChipProps } from '@mui/material'
import { RiskLevel } from '@/types'

interface RiskBadgeProps extends Omit<ChipProps, 'label' | 'color'> {
  riskLevel: RiskLevel
}

const riskColors: Record<RiskLevel, { color: ChipProps['color']; label: string }> = {
  Low: { color: 'success', label: 'Low' },
  Medium: { color: 'warning', label: 'Medium' },
  High: { color: 'error', label: 'High' },
}

export default function RiskBadge({ riskLevel, ...props }: RiskBadgeProps) {
  const config = riskColors[riskLevel]
  return (
    <Chip
      label={config.label}
      color={config.color}
      size="small"
      sx={{ fontWeight: 500 }}
      {...props}
    />
  )
}
