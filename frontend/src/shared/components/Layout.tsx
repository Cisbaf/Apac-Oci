'use client';
import { ReactNode } from "react";
import { useGlobalComponents } from "../context/GlobalUIContext";
import { UserContextProvider } from "../context/UserContext";
import { Box } from "@mui/material";
import AppBarMobile from "./AppBarMobile";
import BreadCumbs from "./BreadCumbs";
import Sidebar from "./SideBar";

interface LayoutProps {
    children: ReactNode;
}

export default function LayoutSystem({children}: LayoutProps) {
    const { shouldShowLayout, isMobile, isTablet } = useGlobalComponents().hookLayout;
    
    return (
        <>
            {shouldShowLayout ? (
            <UserContextProvider>
                {(isMobile || isTablet)?
                    <>
                    <AppBarMobile/>
                    <Box sx={{
                        width: "100%",
                        display: "flex",
                        flexDirection: "column",
                        gap: 2,
                        padding: 1,
                    }}> 
                        <BreadCumbs/>
                        {children}
                    </Box>
                    </> :
                // PC
                <Box sx={{display: "flex"}}>
                    <Sidebar/>

                    <Box sx={{
                        width: "100%",
                        padding: 2,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        gap: 5
                    }}>
                        <Box sx={{ width: "80%"}}>
                            <BreadCumbs/>
                        </Box>
                        <Box sx={{
                            width: "80%",
                            maxHeight: "80vh",
                            overflow: "auto"
                        }}>
                            {children}
                        </Box>
                    </Box>
                </Box>}

            </UserContextProvider>
        ): children}
        </>
    )
}