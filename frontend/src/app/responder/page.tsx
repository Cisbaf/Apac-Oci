"use client";
import React from "react";
import ApacFilter from "@/shared/components/ApacFilter";
import ApacTable from "@/shared/components/ApacTable";
import ApacViewProvider from "@/shared/context/ApacViewContext";
import { AuthorizationProvider } from "../responder/apacAuthorization/context/authorizationContext";
import { Box, Typography, Divider } from "@mui/material";
import { HowToReg } from "@mui/icons-material";
import { RouteGuard } from "@/shared/components/RouteGuard";
import { UserRole } from "@/shared/schemas/user";

export default function ApacAuthorizePage() {
    return(
        <RouteGuard
            allowedRoles={[UserRole.AUTHORIZER, UserRole.ADMIN]}>
            <Box sx={{ display: "flex", flexDirection: "column"}}>
                <Box sx={{ display: "flex", alignItems: "center", gap: 4}}>
                    <HowToReg sx={{fontSize: 32}}/>
                    <Typography variant='h6'>Autorizar Solicitações APAC OCI</Typography>
                </Box>
                <Divider sx={{mt: 1, mb: 2}}/>
                <ApacViewProvider>
                    <AuthorizationProvider>
                        <ApacFilter/>
                        <ApacTable/>
                    </AuthorizationProvider>
                </ApacViewProvider>
            </Box>
        </RouteGuard>
    )
}