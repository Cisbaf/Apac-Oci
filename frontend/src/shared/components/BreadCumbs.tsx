'use client';

import React from 'react';
import { Box, Breadcrumbs, Link, Typography } from "@mui/material";
import { usePathname } from 'next/navigation';

export default function BreadCumbs() {
  const pathname = usePathname(); // ex: "/solicitar"
  
  // Mapeamento de rotas para títulos
  const PageTitle: { [key: string]: string } = {
    'solicitar': 'Solicitar APAC OCI',
    'visualizar': 'Visualizar Registros',
    'responder': 'Autorizar ou Rejeitar APAC',
    'extracao': "Extrair APAC's autorizadas"
  };

  // Extrai o último segmento da URL
  const getTitle = () => {
    const segments = pathname?.split('/').filter(Boolean) || [];
    const lastSegment = segments[segments.length - 1] || '';
    return PageTitle[lastSegment] || lastSegment;
  };

  return (
    <Box>
      <Breadcrumbs aria-label="breadcrumb">
        <Link underline="hover" color="inherit" href="/">
          APAC
        </Link>
        {pathname !== '/' && (
          <Typography color="text.primary">
            {getTitle()}
          </Typography>
        )}
      </Breadcrumbs>
    </Box>
  );
}
