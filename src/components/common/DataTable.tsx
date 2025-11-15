import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  Typography,
} from '@mui/material'
import { ReactNode } from 'react'

export interface Column<T> {
  id: string
  label: string
  minWidth?: number
  align?: 'right' | 'left' | 'center'
  render?: (value: any, row: T) => ReactNode
}

interface DataTableProps<T> {
  columns: Column<T>[]
  rows: T[]
  onRowClick?: (row: T) => void
  emptyMessage?: string
}

export default function DataTable<T extends { id?: string }>({
  columns,
  rows,
  onRowClick,
  emptyMessage = 'No data available',
}: DataTableProps<T>) {
  return (
    <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <TableCell
                key={column.id}
                align={column.align || 'left'}
                style={{ minWidth: column.minWidth }}
                sx={{ fontWeight: 600, backgroundColor: 'background.paper' }}
              >
                {column.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.length === 0 ? (
            <TableRow>
              <TableCell colSpan={columns.length} align="center" sx={{ py: 4 }}>
                <Typography variant="body2" color="text.secondary">
                  {emptyMessage}
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            rows.map((row, index) => (
              <TableRow
                hover
                key={row.id || index}
                onClick={() => onRowClick?.(row)}
                sx={{
                  cursor: onRowClick ? 'pointer' : 'default',
                  '&:hover': onRowClick ? { backgroundColor: 'action.hover' } : {},
                }}
              >
                {columns.map((column) => {
                  const value = (row as any)[column.id]
                  return (
                    <TableCell key={column.id} align={column.align || 'left'}>
                      {column.render ? column.render(value, row) : value}
                    </TableCell>
                  )
                })}
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  )
}
