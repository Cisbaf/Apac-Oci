// src/components/GlobalAlert.tsx
'use client'

import { Alert, AlertProps, Snackbar, SnackbarCloseReason, SnackbarOrigin } from '@mui/material'
import { Grow, GrowProps } from '@mui/material'
import { ReactNode, SyntheticEvent, useEffect, useState } from 'react'

type SnackbarTransitionProps = GrowProps & { children: React.ReactElement<any, any> }

interface GlobalAlertProps extends AlertProps {
  open: boolean
  message: ReactNode
  onClose?: (event?: Event | SyntheticEvent, reason?: SnackbarCloseReason) => void
  autoHideDuration?: number
  anchorOrigin?: SnackbarOrigin
  TransitionComponent?: React.ComponentType<SnackbarTransitionProps>
  TransitionProps?: SnackbarTransitionProps
  snackbarKey?: string | number
}

export default function GlobalAlert({
  open,
  onClose,
  message,
  autoHideDuration = 6000,
  anchorOrigin = { vertical: 'top', horizontal: 'center' },
  TransitionComponent = Grow,
  TransitionProps,
  snackbarKey,
  severity = 'info',
  variant = 'filled',
  ...alertProps
}: GlobalAlertProps) {
  const [isOpen, setIsOpen] = useState(open)

  useEffect(() => {
    setIsOpen(open)
  }, [open])

  const handleClose = (event?: Event | SyntheticEvent, reason?: SnackbarCloseReason) => {
    setIsOpen(false)
    onClose?.(event, reason)
  }

  return (
    <Snackbar
      key={snackbarKey || message?.toString()}
      open={isOpen}
      autoHideDuration={autoHideDuration}
      onClose={handleClose}
      anchorOrigin={anchorOrigin}
      sx={{ maxWidth: '90vw' }}
      ClickAwayListenerProps={{
        mouseEvent: false,
        touchEvent: false,
      }}
    >
      <Alert
        onClose={handleClose}
        severity={severity}
        variant={variant}
        {...alertProps}
        sx={{
          zIndex: 100000,
          alignItems: 'center', // Exemplo de customização do Alert
          ...alertProps.sx,
        }}
      >
        {message}
      </Alert>
    </Snackbar>
  )
}