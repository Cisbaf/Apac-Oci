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