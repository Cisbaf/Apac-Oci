"use client";

import React from 'react';
import {
  Stepper,
  Step,
  StepLabel,
  Typography,
  Box,
  StepConnector,
  styled,
  Button,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
import CancelIcon from '@mui/icons-material/Cancel';
import { ApacStatus } from '@/app/solicitar/apacRequest/schemas/apacRequest';

export const ApacStatusTranslation: Record<ApacStatus, string> = {
  [ApacStatus.PENDING]: 'Pendente',
  [ApacStatus.APPROVED]: 'Aprovado',
  [ApacStatus.REJECTED]: 'Rejeitado',
};

const steps = ['Solicitação OCI realizada', 'Aguardando Avaliação', 'Resultado'];

interface Props {
  status: ApacStatus;
  rejectionReason?: string;
}

const ColorlibConnector = styled(StepConnector)(({ theme }) => ({
  '& .MuiStepConnector-line': {
    height: 3,
    border: 0,
    backgroundColor: theme.palette.mode === 'dark' ? '#444' : '#ccc',
    borderRadius: 1,
  },
}));

const ApacStatusStepper: React.FC<Props> = ({ status, rejectionReason }) => {
  const getActiveStep = () => {
    switch (status) {
      case ApacStatus.PENDING:
        return 1;
      case ApacStatus.APPROVED:
      case ApacStatus.REJECTED:
        return 2;
      default:
        return 0;
    }
  };

  const activeStep = getActiveStep();

  const getIcon = (stepIndex: number) => {
    if (stepIndex < activeStep) return <CheckCircleIcon color="success" />;

    if (stepIndex === activeStep) {
      if (status === ApacStatus.REJECTED) return <CancelIcon color="error" />;
      if (status === ApacStatus.APPROVED) return <CheckCircleIcon color="success" />;
      return <HourglassEmptyIcon color="warning" />;
    }

    return <HourglassEmptyIcon color="disabled" />;
  };

  return (
    <Box sx={{ width: '100%', p: 2 }}>

      <Stepper alternativeLabel activeStep={activeStep} connector={<ColorlibConnector />}>
        {steps.map((label, index) => (
          <Step key={label}>
            <StepLabel StepIconComponent={() => getIcon(index)}>
              {label}
            </StepLabel>
          </Step>
        ))}
      </Stepper>
      {status === ApacStatus.REJECTED && rejectionReason && (
        <Typography color="error" mt={2}>
          Motivo da rejeição: {rejectionReason}
        </Typography>
      )}
    </Box>
  );
};

export default ApacStatusStepper;
