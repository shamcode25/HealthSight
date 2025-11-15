import { createBrowserRouter, Navigate } from 'react-router-dom'
import AppLayout from '@/components/layout/AppLayout'
import OverviewPage from '@/pages/OverviewPage'
import QualitySafetyPage from '@/pages/QualitySafetyPage'
import ReadmissionsPage from '@/pages/ReadmissionsPage'
import DataQualityPage from '@/pages/DataQualityPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/overview" replace />,
      },
      {
        path: 'overview',
        element: <OverviewPage />,
      },
      {
        path: 'quality-safety',
        element: <QualitySafetyPage />,
      },
      {
        path: 'readmissions',
        element: <ReadmissionsPage />,
      },
      {
        path: 'data-quality',
        element: <DataQualityPage />,
      },
      {
        path: 'exports',
        element: (
          <div style={{ padding: '2rem' }}>
            <h2>Exports</h2>
            <p>Export functionality coming soon...</p>
          </div>
        ),
      },
    ],
  },
])
