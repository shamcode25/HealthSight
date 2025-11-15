import { useEffect, useState } from 'react'
import { Grid, Box } from '@mui/material'
import KpiCard from '@/components/common/KpiCard'
import SectionCard from '@/components/common/SectionCard'
import DataTable, { Column } from '@/components/common/DataTable'
import BarChart from '@/components/charts/BarChart'
import {
  fetchDataQualityMetrics,
  fetchDataQualityRecords,
  fetchDataQualityByUnit,
} from '@/services/apiClient'
import { KPIMetric, DataQualityIssue, ChartDataPoint } from '@/types'
import { format } from 'date-fns'

export default function DataQualityPage() {
  const [kpis, setKpis] = useState<Record<string, KPIMetric>>({})
  const [issues, setIssues] = useState<DataQualityIssue[]>([])
  const [unitData, setUnitData] = useState<ChartDataPoint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      setLoading(true)
      try {
        const [kpiData, issueData, unitDataResult] = await Promise.all([
          fetchDataQualityMetrics(),
          fetchDataQualityRecords(),
          fetchDataQualityByUnit(),
        ])
        setKpis(kpiData)
        setIssues(issueData.sort((a, b) => {
          const severityOrder = { High: 3, Medium: 2, Low: 1 }
          return severityOrder[b.severity] - severityOrder[a.severity]
        }))
        setUnitData(unitDataResult)
      } catch (error) {
        console.error('Error loading data quality data:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const issueColumns: Column<DataQualityIssue>[] = [
    { id: 'recordId', label: 'Record ID', minWidth: 100 },
    { id: 'unit', label: 'Unit', minWidth: 120 },
    {
      id: 'issueType',
      label: 'Issue Type',
      minWidth: 100,
      render: (value) => (
        <Box
          sx={{
            px: 1,
            py: 0.5,
            borderRadius: 1,
            display: 'inline-block',
            bgcolor: 'warning.light',
            color: 'warning.dark',
            fontWeight: 500,
            fontSize: '0.75rem',
          }}
        >
          {value}
        </Box>
      ),
    },
    { id: 'field', label: 'Field', minWidth: 150 },
    { id: 'description', label: 'Description', minWidth: 200 },
    {
      id: 'severity',
      label: 'Severity',
      minWidth: 100,
      render: (value) => (
        <Box
          sx={{
            px: 1,
            py: 0.5,
            borderRadius: 1,
            display: 'inline-block',
            bgcolor:
              value === 'High'
                ? 'error.light'
                : value === 'Medium'
                ? 'warning.light'
                : 'success.light',
            color:
              value === 'High'
                ? 'error.dark'
                : value === 'Medium'
                ? 'warning.dark'
                : 'success.dark',
            fontWeight: 500,
            fontSize: '0.75rem',
          }}
        >
          {value}
        </Box>
      ),
    },
    {
      id: 'lastUpdated',
      label: 'Last Updated',
      minWidth: 120,
      render: (value) => format(new Date(value), 'MMM dd, yyyy'),
    },
  ]

  if (loading) {
    return <Box sx={{ p: 3 }}>Loading...</Box>
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {/* KPI Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={kpis.invalidRecords || {}} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={kpis.missingFields || {}} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={kpis.duplicates || {}} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard metric={kpis.staleEpisodes || {}} />
        </Grid>

        {/* Data Quality by Unit Chart */}
        <Grid item xs={12}>
          <SectionCard
            title="Data Quality by Unit"
            subtitle="Issues breakdown by unit"
          >
            <BarChart
              data={unitData}
              bars={[
                { dataKey: 'invalid', name: 'Invalid', color: '#ef4444' },
                { dataKey: 'missing', name: 'Missing', color: '#f59e0b' },
                { dataKey: 'duplicates', name: 'Duplicates', color: '#8b5cf6' },
                { dataKey: 'stale', name: 'Stale', color: '#6b7280' },
              ]}
              height={350}
            />
          </SectionCard>
        </Grid>

        {/* Worst Quality Records Table */}
        <Grid item xs={12}>
          <SectionCard
            title="Data Quality Issues"
            subtitle="Records requiring attention"
          >
            <DataTable columns={issueColumns} rows={issues} />
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  )
}
