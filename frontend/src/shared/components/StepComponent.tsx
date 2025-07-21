// StepComponent.tsx
import React from "react";
import { Box } from "@mui/material";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";
import { FormRepository } from "@/shared/repositories/formRepository";

export interface StepFormValidate {
  validateStep: () => boolean;
}

type RefComponentProps = {
  ref?: React.Ref<FormRepository>;
};

type StepFormProps = {
  children: React.ReactElement<RefComponentProps> | React.ReactElement<RefComponentProps>[];
};
const StepForm = React.forwardRef<StepFormValidate, StepFormProps>((props, ref) => {
  const { showAlert } = useGlobalComponents();
  const refs = React.useRef<(FormRepository | null)[]>([]);

  React.useImperativeHandle(ref, () => ({
    validateStep: () => {
      let isValid = true;
      refs.current.forEach(ref => {
        if (!ref) return;
        const validation = ref.validate();
        if (validation && !validation.success) {
          showAlert({ color: "error", message: validation.message || "" });
          isValid = false;
        }
      });
      return isValid;
    },
  }));

  const childrenArray = React.Children.toArray(props.children) as React.ReactElement<RefComponentProps>[];

  refs.current = childrenArray.map(() => null);

  const childrenWithRefs = childrenArray.map((child, index) => {
    return React.cloneElement(child, {
      ref: (el: FormRepository | null) => {
        refs.current[index] = el;
      },
      key: index,
    });
  });

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
      {childrenWithRefs}
    </Box>
  );
});


export default StepForm;