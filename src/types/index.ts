export type RiskLevel = 'Low' | 'Medium' | 'High'

export interface KPIMetric {
  label: string
  value: string | number
  riskLevel?: RiskLevel
  change?: string
  trend?: 'up' | 'down'
}

export interface PatientEpisode {
  id: string
  patientId: string
  patientName: string
  unit: string
  admissionDate: string
  dischargeDate?: string
  riskLevel: RiskLevel
  los?: number // Length of Stay
  diagnosis: string
  summary?: string
  riskExplanation?: string
  nextBestAction?: string
}

export interface SafetyIncident {
  id: string
  date: string
  category: string
  severity: 'Low' | 'Medium' | 'High' | 'Critical'
  description: string
  unit: string
  status: string
}

export interface DataQualityIssue {
  id: string
  recordId: string
  unit: string
  issueType: 'Invalid' | 'Missing' | 'Duplicate' | 'Stale'
  field: string
  description: string
  severity: 'Low' | 'Medium' | 'High'
  lastUpdated: string
}

export interface ChartDataPoint {
  name: string
  value: number
  [key: string]: string | number
}

export interface RiskDistribution {
  riskLevel: RiskLevel
  count: number
  percentage: number
}
