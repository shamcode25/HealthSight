import { useEffect, useState } from 'react'
import { Grid, Box, Drawer, Typography, Button, MenuItem, Select, FormControl, InputLabel, CircularProgress, Alert } from '@mui/material'
import DataTable, { Column } from '@/components/common/DataTable'
import RiskBadge from '@/components/common/RiskBadge'
import SectionCard from '@/components/common/SectionCard'
import { fetchReadmissionRisks, fetchPatientEpisodeById, generateAllInsights, AIInsights } from '@/services/apiClient'
import { PatientEpisode, RiskLevel } from '@/types'
import { format } from 'date-fns'

export default function ReadmissionsPage() {
  const [episodes, setEpisodes] = useState<PatientEpisode[]>([])
  const [filteredEpisodes, setFilteredEpisodes] = useState<PatientEpisode[]>([])
  const [selectedEpisode, setSelectedEpisode] = useState<PatientEpisode | null>(null)
  const [aiInsights, setAiInsights] = useState<AIInsights | null>(null)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [unitFilter, setUnitFilter] = useState<string>('All')
  const [riskFilter, setRiskFilter] = useState<string>('All')
  const [loading, setLoading] = useState(true)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState<string | null>(null)

  useEffect(() => {
    const loadData = async () => {
      setLoading(true)
      try {
        const unit = unitFilter !== 'All' ? unitFilter : undefined
        const riskLevel = riskFilter !== 'All' ? riskFilter : undefined
        const data = await fetchReadmissionRisks(unit, riskLevel)
        setEpisodes(data)
        setFilteredEpisodes(data)
      } catch (error) {
        console.error('Error loading readmission data:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [unitFilter, riskFilter])

  const handleRowClick = async (episode: PatientEpisode) => {
    // Load episode data
    const fullEpisode = await fetchPatientEpisodeById(episode.id)
    if (fullEpisode) {
      setSelectedEpisode(fullEpisode)
      setDrawerOpen(true)
      setAiInsights(null)
      setAiError(null)
      
      // Generate AI insights
      setAiLoading(true)
      try {
        const insights = await generateAllInsights(episode.id)
        setAiInsights(insights)
        
        // Update episode with AI-generated content if available
        if (insights.summary || insights.risk_explanation || insights.recommendations) {
          const updatedEpisode = {
            ...fullEpisode,
            summary: insights.summary || fullEpisode.summary,
            riskExplanation: insights.risk_explanation || fullEpisode.riskExplanation,
            nextBestAction: insights.recommendations || fullEpisode.nextBestAction,
          }
          setSelectedEpisode(updatedEpisode)
        }
      } catch (error: any) {
        console.error('Error generating AI insights:', error)
        setAiError(
          error.response?.data?.detail || 
          error.message || 
          'Failed to generate AI insights. Please try again.'
        )
      } finally {
        setAiLoading(false)
      }
    }
  }

  const handleCloseDrawer = () => {
    setDrawerOpen(false)
    setSelectedEpisode(null)
    setAiInsights(null)
    setAiError(null)
  }

  const columns: Column<PatientEpisode>[] = [
    { id: 'id', label: 'Episode ID', minWidth: 100 },
    { id: 'patientName', label: 'Patient Name', minWidth: 150 },
    { id: 'unit', label: 'Unit', minWidth: 120 },
    {
      id: 'admissionDate',
      label: 'Admission Date',
      minWidth: 120,
      render: (value) => format(new Date(value), 'MMM dd, yyyy'),
    },
    {
      id: 'dischargeDate',
      label: 'Discharge Date',
      minWidth: 120,
      render: (value) => (value ? format(new Date(value), 'MMM dd, yyyy') : 'Active'),
    },
    { id: 'diagnosis', label: 'Diagnosis', minWidth: 200 },
    {
      id: 'riskLevel',
      label: 'Risk Level',
      minWidth: 100,
      render: (value: RiskLevel) => <RiskBadge riskLevel={value} />,
    },
  ]

  const units = Array.from(new Set(episodes.map((e) => e.unit)))

  if (loading) {
    return <Box sx={{ p: 3 }}>Loading...</Box>
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Filters */}
        <Grid item xs={12}>
          <SectionCard title="High-Risk Patient Episodes" subtitle="Monitor and manage readmission risks">
            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
              <FormControl sx={{ minWidth: 200 }}>
                <InputLabel>Unit</InputLabel>
                <Select
                  value={unitFilter}
                  label="Unit"
                  onChange={(e) => setUnitFilter(e.target.value)}
                >
                  <MenuItem value="All">All Units</MenuItem>
                  {units.map((unit) => (
                    <MenuItem key={unit} value={unit}>
                      {unit}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl sx={{ minWidth: 200 }}>
                <InputLabel>Risk Level</InputLabel>
                <Select
                  value={riskFilter}
                  label="Risk Level"
                  onChange={(e) => setRiskFilter(e.target.value)}
                >
                  <MenuItem value="All">All Levels</MenuItem>
                  <MenuItem value="Low">Low</MenuItem>
                  <MenuItem value="Medium">Medium</MenuItem>
                  <MenuItem value="High">High</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <DataTable columns={columns} rows={filteredEpisodes} onRowClick={handleRowClick} />
          </SectionCard>
        </Grid>
      </Grid>

      {/* Episode Detail Drawer */}
      <Drawer anchor="right" open={drawerOpen} onClose={handleCloseDrawer}>
        <Box sx={{ width: 500, p: 3 }}>
          {selectedEpisode && (
            <>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                Episode Details
              </Typography>

              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Episode ID
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {selectedEpisode.id}
                </Typography>

                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Patient
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {selectedEpisode.patientName} (ID: {selectedEpisode.patientId})
                </Typography>

                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Unit
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {selectedEpisode.unit}
                </Typography>

                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Risk Level
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <RiskBadge riskLevel={selectedEpisode.riskLevel} />
                </Box>

                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Diagnosis
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {selectedEpisode.diagnosis}
                </Typography>
              </Box>

              {/* AI Loading State */}
              {aiLoading && (
                <Box sx={{ mb: 3, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
                  <CircularProgress size={40} />
                  <Typography variant="body2" color="text.secondary">
                    Generating AI insights...
                  </Typography>
                </Box>
              )}

              {/* AI Error State */}
              {aiError && !aiLoading && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {aiError}
                </Alert>
              )}

              {/* Summary Section */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Summary
                  {aiInsights?.summary && (
                    <Typography component="span" variant="caption" sx={{ ml: 1, color: 'primary.main' }}>
                      (AI Generated)
                    </Typography>
                  )}
                </Typography>
                {aiLoading && !selectedEpisode.summary ? (
                  <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                    Generating summary...
                  </Typography>
                ) : (
                  <Typography variant="body1" color="text.secondary">
                    {aiInsights?.summary || selectedEpisode.summary || 'No summary available. Click to generate AI summary.'}
                  </Typography>
                )}
              </Box>

              {/* Risk Explanation Section */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Risk Explanation
                  {aiInsights?.risk_explanation && (
                    <Typography component="span" variant="caption" sx={{ ml: 1, color: 'primary.main' }}>
                      (AI Generated)
                    </Typography>
                  )}
                </Typography>
                {aiLoading && !selectedEpisode.riskExplanation ? (
                  <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                    Generating risk explanation...
                  </Typography>
                ) : (
                  <Typography variant="body1" color="text.secondary">
                    {aiInsights?.risk_explanation || selectedEpisode.riskExplanation || 'No risk explanation available. Click to generate AI explanation.'}
                  </Typography>
                )}
              </Box>

              {/* Next Best Action / Recommendations Section */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Next Best Action
                  {aiInsights?.recommendations && (
                    <Typography component="span" variant="caption" sx={{ ml: 1, color: 'primary.main' }}>
                      (AI Generated)
                    </Typography>
                  )}
                </Typography>
                {aiLoading && !selectedEpisode.nextBestAction ? (
                  <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                    Generating recommendations...
                  </Typography>
                ) : (
                  <Typography variant="body1" color="text.secondary" sx={{ whiteSpace: 'pre-line' }}>
                    {aiInsights?.recommendations || selectedEpisode.nextBestAction || 'No recommendations available. Click to generate AI recommendations.'}
                  </Typography>
                )}
              </Box>

              {/* AI Generation Timestamp */}
              {aiInsights?.generated_at && (
                <Typography variant="caption" color="text.secondary" sx={{ mb: 2, display: 'block' }}>
                  AI insights generated: {format(new Date(aiInsights.generated_at), 'MMM dd, yyyy HH:mm')}
                </Typography>
              )}

              <Button variant="contained" fullWidth onClick={handleCloseDrawer} sx={{ mt: 2 }}>
                Close
              </Button>
            </>
          )}
        </Box>
      </Drawer>
    </Box>
  )
}
