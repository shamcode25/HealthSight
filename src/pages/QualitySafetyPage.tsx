import { useEffect, useState } from 'react'
import { Grid, Box } from '@mui/material'
import KpiCard from '@/components/common/KpiCard'
import SectionCard from '@/components/common/SectionCard'
import DataTable, { Column } from '@/components/common/DataTable'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import {
  fetchSafetyKPIs,
  fetchSafetyIncidents,
  fetchIncidentCategoryData,
} from '@/services/apiClient'
import { KPIMetric, SafetyIncident, ChartDataPoint } from '@/types'

export default function QualitySafetyPage() {
  const [kpis, setKpis] = useState<Record<string, KPIMetric>>({})
  const [incidents, setIncidents] = useState<SafetyIncident[]>([])
  const [categoryData, setCategoryData] = useState<ChartDataPoint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      setLoading(true)
      try {
        const [kpiData, incidentData, categoryDataResult] = await Promise.all([
          fetchSafetyKPIs(),
          fetchSafetyIncidents(),
          fetchIncidentCategoryData(),
        ])
        setKpis(kpiData)
        setIncidents(incidentData.filter((i) => i.severity === 'High' || i.severity === 'Critical'))
        setCategoryData(categoryDataResult)
      } catch (error) {
        console.error('Error loading safety data:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const incidentColumns: Column<SafetyIncident>[] = [
    { id: 'date', label: 'Date', minWidth: 100 },
    { id: 'category', label: 'Category', minWidth: 120 },
    { id: 'severity', label: 'Severity', minWidth: 100, render: (value) => (
      <Box
        sx={{
          px: 1,
          py: 0.5,
          borderRadius: 1,
          display: 'inline-block',
          bgcolor:
            value === 'Critical' || value === 'High'
              ? 'error.light'
              : value === 'Medium'
              ? 'warning.light'
              : 'success.light',
          color:
            value === 'Critical' || value === 'High'
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
    ) },
    { id: 'description', label: 'Description', minWidth: 200 },
    { id: 'unit', label: 'Unit', minWidth: 100 },
    { id: 'status', label: 'Status', minWidth: 100 },
  ]

  if (loading) {
    return <Box sx={{ p: 3 }}>Loading...</Box>
  }

  const COLORS = ['#ef4444', '#f59e0b', '#8b5cf6', '#3b82f6', '#6b7280']

  return (
    <Box>
      <Grid container spacing={3}>
        {/* KPI Cards */}
        <Grid item xs={12} sm={4}>
          <KpiCard metric={kpis.falls || {}} />
        </Grid>
        <Grid item xs={12} sm={4}>
          <KpiCard metric={kpis.medErrors || {}} />
        </Grid>
        <Grid item xs={12} sm={4}>
          <KpiCard metric={kpis.incidents || {}} />
        </Grid>

        {/* Incident Category Pie Chart */}
        <Grid item xs={12} md={6}>
          <SectionCard
            title="Incident Categories"
            subtitle="Distribution by category"
          >
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }: { name: string; percent: number }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {categoryData.map((_entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </SectionCard>
        </Grid>

        {/* High Severity Events Table */}
        <Grid item xs={12} md={6}>
          <SectionCard
            title="High-Severity Events"
            subtitle="Critical and high-severity incidents"
          >
            <DataTable columns={incidentColumns} rows={incidents} />
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  )
}
