import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box, Typography } from '@mui/material'
import { useLocation, useNavigate } from 'react-router-dom'
import DashboardIcon from '@mui/icons-material/Dashboard'
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety'
import RepeatIcon from '@mui/icons-material/Repeat'
import AssessmentIcon from '@mui/icons-material/Assessment'
import FileDownloadIcon from '@mui/icons-material/FileDownload'
import LocalHospitalIcon from '@mui/icons-material/LocalHospital'

const drawerWidth = 240

const menuItems = [
  { path: '/overview', label: 'Overview', icon: DashboardIcon },
  { path: '/quality-safety', label: 'Quality & Safety', icon: HealthAndSafetyIcon },
  { path: '/readmissions', label: 'Readmissions', icon: RepeatIcon },
  { path: '/data-quality', label: 'Data Quality', icon: AssessmentIcon },
  { path: '/exports', label: 'Exports', icon: FileDownloadIcon },
]

export default function Sidebar() {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
    >
      <Box sx={{ p: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <LocalHospitalIcon sx={{ color: 'primary.main', fontSize: 28 }} />
          <Typography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>
            HealthSight
          </Typography>
        </Box>
      </Box>
      <List sx={{ pt: 2 }}>
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                selected={isActive}
                onClick={() => navigate(item.path)}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: 'primary.main',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: 'primary.dark',
                    },
                    '& .MuiListItemIcon-root': {
                      color: 'white',
                    },
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color: isActive ? 'white' : 'text.secondary',
                    minWidth: 40,
                  }}
                >
                  <Icon />
                </ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          )
        })}
      </List>
    </Drawer>
  )
}
