// src/hooks/useGlobalLayout.ts
'use client'

import { usePathname } from 'next/navigation'
import { useTheme, useMediaQuery } from '@mui/material'
import { useState, useEffect } from 'react'

// Defina aqui as páginas que não devem exibir layout
const PAGES_WITHOUT_LAYOUT: string[] = [
  '/login',
  '/register',
  // adicione outras páginas se necessário
]

export function useGlobalLayout() {
  const pathname = usePathname()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'))
  const shouldShowLayout = !PAGES_WITHOUT_LAYOUT.includes(pathname)

  const [windowSize, setWindowSize] = useState({ width: 0, height: 0 })

  useEffect(() => {
    function handleResize() {
      setWindowSize({ width: window.innerWidth, height: window.innerHeight })
    }

    handleResize() // Define o tamanho inicial
    window.addEventListener('resize', handleResize)

    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return {
    pathname,
    theme,
    isMobile,
    isTablet,
    shouldShowLayout,
    windowSize,
  }
}
