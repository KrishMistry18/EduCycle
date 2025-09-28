import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const RegisterPage = () => {
  return (
    <Box sx={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Paper sx={{ p: 4, maxWidth: 400 }}>
        <Typography variant="h4" gutterBottom>
          Register Page
        </Typography>
        <Typography variant="body1">
          Registration form will be implemented here.
        </Typography>
      </Paper>
    </Box>
  );
};

export default RegisterPage;
