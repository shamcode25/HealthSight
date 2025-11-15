import { Box, Typography } from '@mui/material'
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import { ChartDataPoint } from '@/types'

interface HeatmapChartProps {
  data: ChartDataPoint[]
  title?: string
  xAxisKey?: string
  dataKey: string
  colorKey?: string
  height?: number
}

const getColorIntensity = (value: number, max: number) => {
  const intensity = value / max
  if (intensity < 0.33) return '#3b82f6' // Light blue
  if (intensity < 0.66) return '#f59e0b' // Orange
  return '#ef4444' // Red
}

export default function HeatmapChart({
  data,
  title,
  xAxisKey = 'name',
  dataKey,
  colorKey,
  height = 300,
}: HeatmapChartProps) {
  const maxValue = Math.max(...data.map((d) => (d[dataKey] as number) || 0))

  return (
    <Box>
      {title && (
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
          {title}
        </Typography>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey={xAxisKey} stroke="#6b7280" />
          <YAxis stroke="#6b7280" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Bar dataKey={dataKey} name={dataKey}>
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={colorKey ? (entry[colorKey] as string) : getColorIntensity((entry[dataKey] as number) || 0, maxValue)}
              />
            ))}
          </Bar>
        </RechartsBarChart>
      </ResponsiveContainer>
    </Box>
  )
}
