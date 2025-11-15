import axios from 'axios'
import {
  PatientEpisode,
  SafetyIncident,
  DataQualityIssue,
  ChartDataPoint,
  RiskDistribution,
  KPIMetric,
} from '../types'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const fetchOverviewMetrics = async (): Promise<Record<string, KPIMetric>> => {
  const res = await api.get('/overview-metrics')
  return res.data
}

export const fetchRiskDistribution = async (): Promise<RiskDistribution[]> => {
  const res = await api.get('/risk-distribution')
  return res.data.map((item: { name: string; value: number; color: string }) => ({
    riskLevel: item.name as 'Low' | 'Medium' | 'High',
    count: item.value,
    percentage: 0, // Calculate if needed
  }))
}

export const fetchRiskDistributionChart = async (): Promise<ChartDataPoint[]> => {
  const res = await api.get('/risk-distribution')
  return res.data.map((item: { name: string; value: number; color: string }) => ({
    name: item.name,
    value: item.value,
    color: item.color,
  }))
}

export const fetchHealthTrendData = async (): Promise<ChartDataPoint[]> => {
  const res = await api.get('/health-trends')
  return res.data
}

export const fetchReadmissionRisks = async (unit?: string, riskLevel?: string): Promise<PatientEpisode[]> => {
  const params: Record<string, string> = {}
  if (unit) params.unit = unit
  if (riskLevel) params.risk_level = riskLevel
  
  const res = await api.get('/readmissions/list', { params })
  return res.data.map((ep: any) => ({
    id: ep.id,
    patientId: ep.patientId,
    patientName: ep.patientName,
    unit: ep.unit,
    admissionDate: ep.admissionDate,
    dischargeDate: ep.dischargeDate,
    riskLevel: ep.riskLevel as 'Low' | 'Medium' | 'High',
    los: ep.los,
    diagnosis: ep.diagnosis,
    summary: ep.summary,
    riskExplanation: ep.riskExplanation,
    nextBestAction: ep.nextBestAction,
  }))
}

export const fetchSafetyIncidents = async (): Promise<SafetyIncident[]> => {
  const res = await api.get('/quality/incidents')
  return res.data.map((inc: any) => ({
    id: inc.id,
    date: inc.date,
    category: inc.category,
    severity: inc.severity as 'Low' | 'Medium' | 'High' | 'Critical',
    description: inc.description,
    unit: inc.unit,
    status: inc.status,
  }))
}

export const fetchSafetyKPIs = async (): Promise<Record<string, KPIMetric>> => {
  const res = await api.get('/quality/incidents/summary')
  return res.data.kpis
}

export const fetchIncidentCategoryData = async (): Promise<ChartDataPoint[]> => {
  const res = await api.get('/quality/incidents/summary')
  return res.data.categoryData
}

export const fetchDataQualityMetrics = async (): Promise<Record<string, KPIMetric>> => {
  const res = await api.get('/data-quality/metrics')
  return res.data.kpis
}

export const fetchDataQualityRecords = async (): Promise<DataQualityIssue[]> => {
  const res = await api.get('/data-quality/issues')
  return res.data.map((iss: any) => ({
    id: iss.id,
    recordId: iss.recordId,
    unit: iss.unit,
    issueType: iss.issueType as 'Invalid' | 'Missing' | 'Duplicate' | 'Stale',
    field: iss.field,
    description: iss.description,
    severity: iss.severity as 'Low' | 'Medium' | 'High',
    lastUpdated: iss.lastUpdated,
  }))
}

export const fetchDataQualityByUnit = async (): Promise<ChartDataPoint[]> => {
  const res = await api.get('/data-quality/metrics')
  return res.data.byUnit
}

export const fetchPatientEpisodeById = async (id: string): Promise<PatientEpisode | null> => {
  try {
    const res = await api.get(`/readmissions/${id}`)
    const ep = res.data
    return {
      id: ep.id,
      patientId: ep.patientId,
      patientName: ep.patientName,
      unit: ep.unit,
      admissionDate: ep.admissionDate,
      dischargeDate: ep.dischargeDate,
      riskLevel: ep.riskLevel as 'Low' | 'Medium' | 'High',
      los: ep.los,
      diagnosis: ep.diagnosis,
      summary: ep.summary || ep.summary_text,
      riskExplanation: ep.riskExplanation,
      nextBestAction: ep.nextBestAction || ep.recommendations,
    }
  } catch (error) {
    console.error('Error fetching episode:', error)
    return null
  }
}

// AI Generation Functions
export interface AIInsights {
  summary?: string
  risk_explanation?: string
  recommendations?: string
  generated_at?: string
}

export const generateSummary = async (episodeId: string): Promise<AIInsights> => {
  const res = await api.post(`/llm/summary/${episodeId}`)
  return res.data
}

export const generateRiskExplanation = async (episodeId: string): Promise<AIInsights> => {
  const res = await api.post(`/llm/risk-explanation/${episodeId}`)
  return res.data
}

export const generateRecommendations = async (episodeId: string): Promise<AIInsights> => {
  const res = await api.post(`/llm/recommendations/${episodeId}`)
  return res.data
}

export const generateAllInsights = async (episodeId: string): Promise<AIInsights> => {
  const res = await api.post(`/llm/generate-all/${episodeId}`)
  return res.data
}