import { Card, CardContent, Typography, Box, Chip } from '@mui/material'
import { TrendingUp, TrendingDown } from '@mui/icons-material'
import { KPIMetric } from '@/types'
import RiskBadge from './RiskBadge'

interface KpiCardProps {
  metric: KPIMetric
}

export default function KpiCard({ metric }: KpiCardProps) {
  if (!metric) {
    return (
      <Card>
        <CardContent>
          <Typography variant="body2" color="text.secondary">
            Loading...
          </Typography>
        </CardContent>
      </Card>
    )
  }

  const hasTrend = metric.trend && metric.change

  return (
    <Card>
      <CardContent>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {metric.label || 'N/A'}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 1, mt: 1, mb: 2 }}>
          <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
            {metric.value ?? 'N/A'}
          </Typography>
          {hasTrend && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              {metric.trend === 'up' ? (
                <TrendingUp sx={{ fontSize: 16, color: 'success.main' }} />
              ) : (
                <TrendingDown sx={{ fontSize: 16, color: 'error.main' }} />
              )}
              <Typography
                variant="body2"
                sx={{
                  color: metric.trend === 'up' ? 'success.main' : 'error.main',
                  fontWeight: 500,
                }}
              >
                {metric.change}
              </Typography>
            </Box>
          )}
        </Box>
        {metric.riskLevel && (
          <RiskBadge riskLevel={metric.riskLevel} />
        )}
      </CardContent>
    </Card>
  )
}
