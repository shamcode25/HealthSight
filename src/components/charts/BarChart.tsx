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
} from 'recharts'
import { ChartDataPoint } from '@/types'

interface BarChartProps {
  data: ChartDataPoint[]
  title?: string
  xAxisKey?: string
  bars: Array<{
    dataKey: string
    name: string
    color: string
  }>
  height?: number
}

export default function BarChart({
  data,
  title,
  xAxisKey = 'name',
  bars,
  height = 300,
}: BarChartProps) {
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
          {bars.map((bar) => (
            <Bar key={bar.dataKey} dataKey={bar.dataKey} name={bar.name} fill={bar.color} />
          ))}
        </RechartsBarChart>
      </ResponsiveContainer>
    </Box>
  )
}
