'use client';
import { UserContextProvider } from "@/shared/context/UserContext";
import { GlobalComponentsProvider } from "@/shared/context/GlobalUIContext";
import Sidebar from "@/shared/components/SideBar";
import ButtonAppBar from "@/shared/components/AppBar";
import ResponsiveLayout from "@/shared/components/ResponsiveLayout";
import { Box, useMediaQuery, useTheme } from '@mui/material';
import React from "react";
import { usePathname } from 'next/navigation';

// Lista de páginas que não devem mostrar o layout
const PAGES_WITHOUT_LAYOUT = ['/login', '/logout'];

export default function LayoutComponent({children}: {children: React.ReactNode}) {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
    const pathname = usePathname();
    
    // Verifica se a página atual deve mostrar o layout
    const shouldShowLayout = !PAGES_WITHOUT_LAYOUT.includes(pathname);

    return (
        <GlobalComponentsProvider>
            {shouldShowLayout ? (
            <UserContextProvider>
                <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
                    {/* Sidebar à esquerda */}
                    <Sidebar />

                    {/* Conteúdo principal à direita */}
                    <Box
                    sx={{
                        flex: 1,
                        display: "flex",
                        flexDirection: "column",
                        overflow: "hidden",
                    }}
                    >
                    {/* AppBar no topo */}
                    { !isMobile && !isTablet && <ButtonAppBar/>}
                    {/* Área de conteúdo scrollável */}
                    <Box
                        sx={{
                        flex: 1,
                        overflow: "auto",
                        p: { xs: 2, sm: 2 },
                        backgroundColor: "#f6f6f6",
                        display: "flex",
                        }}
                    >
                        <ResponsiveLayout><div style={{
                            backgroundColor: '#fff',
                            borderRadius: 2,
                            boxShadow: "3px",
                            padding: "20px",
                        }}>{children}</div></ResponsiveLayout>
                    </Box>
                    </Box>
                </div>
                </UserContextProvider>
            ) : (
                // Renderiza apenas o conteúdo sem layout para páginas específicas
                children
            )}
        </GlobalComponentsProvider>
    );
}