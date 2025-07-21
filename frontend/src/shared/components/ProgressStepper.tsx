import React, { FC, useCallback, useRef, useState, Children, isValidElement, cloneElement } from "react";
import { Box, Button, LinearProgress, Stack } from "@mui/material";
import { styled } from "@mui/material/styles";
import StepForm, { StepFormValidate } from "@/shared/components/StepComponent";

const ProgressBar = styled(LinearProgress)(({ theme }) => ({
  height: 20,
  borderRadius: 2,
  backgroundColor: theme.palette.grey[300],
  "& .MuiLinearProgress-bar": {
    borderRadius: 2,
    backgroundColor: "theme.palette.primary.main"
  }
}));

interface ProgressStepperProps {
  children: React.ReactNode;
}

export const ProgressStepper: FC<ProgressStepperProps> = ({ children }) => {
  const stepFormRef = useRef<StepFormValidate>(null);
  const [activeStep, setActiveStep] = useState(0);

  const steps = Children.toArray(children).filter(
    (child): child is React.ReactElement<React.ComponentProps<typeof StepForm>> =>
      isValidElement(child) && child.type === StepForm
  );

  const setRef = useCallback((instance: StepFormValidate | null) => {
    stepFormRef.current = instance;
  }, []);

  const validateCurrentStep = () => {
    return stepFormRef.current?.validateStep() ?? false;
  };

  const nextStep = () => {
    if (validateCurrentStep()) {
      setActiveStep((prev) => Math.min(prev + 1, steps.length - 1));
    }
  };

  const prevStep = () => {
    setActiveStep((prev) => Math.max(prev - 1, 0));
  };

  const isFirstStep = activeStep === 0;
  const isLastStep = activeStep === steps.length - 1;
  const progress = ((activeStep + 1) / steps.length) * 100;

  return (
    <>
      <ProgressBar variant="determinate" value={progress} sx={{ mb: 4 }} />

      <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
        {cloneElement(steps[activeStep], { ref: setRef })}

        <Stack direction="row" spacing={2} justifyContent="flex-end">
          {!isFirstStep && (
            <Button variant="outlined" onClick={prevStep} fullWidth={isLastStep}>
              Voltar
            </Button>
          )}
          {!isLastStep && (
            <Button variant="contained"  onClick={nextStep}>
              Próximo
            </Button>
          )}
        </Stack>
      </Box>
    </>
  );
};
