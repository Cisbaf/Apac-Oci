import React, { forwardRef, useImperativeHandle, useRef, useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from "@mui/material";

export interface ConfirmOptions {
  title?: string;
  confirmLabel?: string;
  cancelLabel?: string;
}

export interface ConfirmDialogHandles {
  confirm: (message: string, options?: ConfirmOptions) => Promise<boolean>;
}

interface ConfirmDialogState extends Required<ConfirmOptions> {
  open: boolean;
  message: string;
}

const defaultState: ConfirmDialogState = {
  open: false,
  message: "",
  title: "Atenção",
  confirmLabel: "Continuar mesmo assim",
  cancelLabel: "Corrigir",
};

const ConfirmDialog = forwardRef<ConfirmDialogHandles>((_props, ref) => {
  const [state, setState] = useState<ConfirmDialogState>(defaultState);
  const resolveRef = useRef<((value: boolean) => void) | null>(null);

  useImperativeHandle(ref, () => ({
    confirm: (message, options) =>
      new Promise<boolean>((resolve) => {
        resolveRef.current = resolve;
        setState({
          open: true,
          message,
          title: options?.title || defaultState.title,
          confirmLabel: options?.confirmLabel || defaultState.confirmLabel,
          cancelLabel: options?.cancelLabel || defaultState.cancelLabel,
        });
      }),
  }));

  const handleClose = (result: boolean) => {
    setState((prev) => ({ ...prev, open: false }));
    resolveRef.current?.(result);
    resolveRef.current = null;
  };

  return (
    <Dialog open={state.open} onClose={() => handleClose(false)}>
      <DialogTitle>{state.title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{state.message}</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => handleClose(false)}>{state.cancelLabel}</Button>
        <Button onClick={() => handleClose(true)} variant="contained" color="warning" autoFocus>
          {state.confirmLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
});

ConfirmDialog.displayName = "ConfirmDialog";

export default ConfirmDialog;
