// src/shared/components/ResponsiveLayout.tsx
'use client';
import React from 'react';
import { Box, useMediaQuery, useTheme } from '@mui/material';

interface ResponsiveProps {
  children: React.ReactNode;
}

const ResponsiveLayout: React.FC<ResponsiveProps> = ({ children }) => {
  const theme = useTheme();

  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));


    const getWidth = () => {
      if (!isMobile && !isTablet) return '80%';
      return '100%';
    };

  return (
    <Box
      sx={{
        mx: 'auto',
        width: '100%',
        maxWidth: getWidth(),
        overflowY: 'auto',
        transition: 'height 0.3s ease',
      }}
    >
      {children}
    </Box>
  );
};

export default ResponsiveLayout;
