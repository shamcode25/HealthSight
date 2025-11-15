import { useEffect, useState } from 'react'
import { Grid, Box } from '@mui/material'
import KpiCard from '@/components/common/KpiCard'
import SectionCard from '@/components/common/SectionCard'
import BarChart from '@/components/charts/BarChart'
import LineChart from '@/components/charts/LineChart'
import {
  fetchOverviewMetrics,
  fetchRiskDistributionChart,
  fetchHealthTrendData,
} from '@/services/apiClient'
import { KPIMetric, ChartDataPoint } from '@/types'

export default function OverviewPage() {
  const [metrics, setMetrics] = useState<Record<string, KPIMetric>>({})
  const [riskDistribution, setRiskDistribution] = useState<ChartDataPoint[]>([])
  const [healthTrend, setHealthTrend] = useState<ChartDataPoint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      setLoading(true)
      try {
        const [metricsData, riskData, trendData] = await Promise.all([
          fetchOverviewMetrics(),
          fetchRiskDistributionChart(),
          fetchHealthTrendData(),
        ])
        setMetrics(metricsData)
        setRiskDistribution(riskData)
        setHealthTrend(trendData)
      } catch (error) {
        console.error('Error loading overview data:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  if (loading) {
    return <Box sx={{ p: 3 }}>Loading...</Box>
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {/* KPI Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={metrics.readmissionRate || {}} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={metrics.avgLOS || {}} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={metrics.safetyEvents || {}} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={metrics.dataQualityScore || {}} />
        </Grid>

        {/* Risk Distribution Chart */}
        <Grid item xs={12} md={6}>
          <SectionCard
            title="Risk Distribution"
            subtitle="Current patient risk levels"
          >
            <BarChart
              data={riskDistribution}
              bars={[
                { dataKey: 'value', name: 'Patients', color: '#3b82f6' },
              ]}
              height={300}
            />
          </SectionCard>
        </Grid>

        {/* Health Trend Chart */}
        <Grid item xs={12} md={6}>
          <SectionCard
            title="Health Trends"
            subtitle="Readmissions vs Episodes over time"
          >
            <LineChart
              data={healthTrend}
              lines={[
                { dataKey: 'readmissions', name: 'Readmissions', color: '#ef4444', strokeWidth: 2 },
                { dataKey: 'episodes', name: 'Episodes', color: '#3b82f6', strokeWidth: 2 },
              ]}
              height={300}
            />
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  )
}
