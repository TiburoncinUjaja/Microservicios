import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  CircularProgress,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { flightsApi } from '../services/api';
import type { Flight } from '../types';

export const Flights = () => {
  const { data: flights, isLoading, error } = useQuery<Flight[]>({
    queryKey: ['flights'],
    queryFn: flightsApi.getAll,
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Typography color="error">Error loading flights</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Flights</Typography>
        <Button variant="contained" color="primary">
          Add Flight
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Flight Number</TableCell>
              <TableCell>Origin</TableCell>
              <TableCell>Destination</TableCell>
              <TableCell>Departure</TableCell>
              <TableCell>Arrival</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {flights?.map((flight) => (
              <TableRow key={flight.id}>
                <TableCell>{flight.numero_vuelo}</TableCell>
                <TableCell>{flight.origen_id}</TableCell>
                <TableCell>{flight.destino_id}</TableCell>
                <TableCell>{new Date(flight.fecha_salida).toLocaleString()}</TableCell>
                <TableCell>{new Date(flight.fecha_llegada).toLocaleString()}</TableCell>
                <TableCell>{flight.estado}</TableCell>
                <TableCell>
                  <Button size="small" color="primary">
                    Edit
                  </Button>
                  <Button size="small" color="error">
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}; 