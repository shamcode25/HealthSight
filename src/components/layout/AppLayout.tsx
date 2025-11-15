import { Box } from '@mui/material'
import { Outlet, useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopBar from './TopBar'

const pageTitles: Record<string, string> = {
  '/overview': 'Overview',
  '/quality-safety': 'Quality & Safety',
  '/readmissions': 'Readmissions',
  '/data-quality': 'Data Quality',
  '/exports': 'Exports',
}

export default function AppLayout() {
  const location = useLocation()
  const pageTitle = pageTitles[location.pathname] || 'Healthcare Analytics Dashboard'

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <TopBar pageTitle={pageTitle} />
        <Box component="main" sx={{ flexGrow: 1, p: 3, backgroundColor: 'background.default' }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  )
}
