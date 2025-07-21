// src/contexts/GlobalComponentsContext.tsx
'use client'

import { createContext, useContext, useState } from 'react'
import { AlertProps, Backdrop, CircularProgress, Typography } from '@mui/material'
import GlobalAlert from '@/shared/components/GlobalAlert'

interface GlobalComponentsContextType {
  showAlert: (props: AlertProps & { message: string }) => void;
  showBackdrop: (show: boolean, message?: string) => void;
  showResponseApi: (response: Response) => Promise<any>;
}

const GlobalComponentsContext = createContext<GlobalComponentsContextType | null>(null)

export function GlobalComponentsProvider({ children }: { children: React.ReactNode }) {
  const [backdropOpen, setBackdropOpen] = useState(false)
  const [alertProps, setAlertProps] = useState<AlertProps & { message: string } | null>(null)
  const [message, setMessage] = useState("");

  const showAlert = (props: AlertProps & { message: string }) => {
    setAlertProps(props)
  }

  const showBackdrop = (show: boolean, message?: string) => {
    setBackdropOpen(show)
    if (!show) setMessage("");
    if (show && message) setMessage(message);
  }


  const showResponseApi = async(response: Response) => {
    const json = await response.json();
    if (json.message){
      showAlert({color: response.ok? "success":"error", message: json.message});
    }
    return json;
  }

  const handleCloseAlert = () => {
    setAlertProps(null)
  }

  return (
    <GlobalComponentsContext.Provider value={{ showAlert, showBackdrop, showResponseApi }}>
      {children}
      
      {/* Backdrop Global */}
      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.modal + 10, display: "flex", gap: 2 }}
        open={backdropOpen}
      >
        <CircularProgress color="inherit" />
        <Typography variant='h6'>{message}</Typography>
      </Backdrop>
      
      {/* Alert Global */}
      {alertProps && (
        <GlobalAlert
          {...alertProps}
          open={Boolean(alertProps)}
          onClose={handleCloseAlert}
        />
      )}
    </GlobalComponentsContext.Provider>
  )
}

export function useGlobalComponents() {
  const context = useContext(GlobalComponentsContext)
  if (!context) {
    throw new Error('useGlobalComponents must be used within a GlobalComponentsProvider')
  }
  return context
}