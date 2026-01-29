"use client";
import React from "react";
import ApacFilter from "@/shared/components/ApacFilter";
import ApacTable from "@/shared/components/ApacTable";
import ApacViewProvider from "@/shared/context/ApacViewContext";
import { AuthorizationProvider } from "../responder/apacAuthorization/context/authorizationContext";
import { Box, Typography, Divider } from "@mui/material";
import { RouteGuard } from "@/shared/components/RouteGuard";
import { UserRole } from "@/shared/schemas/user";
import AutorizeMultiplesApacProvider from "@/shared/context/AutorizeMultiplesApac";

export default function ApacAuthorizePage() {
    return(
        <RouteGuard
            allowedRoles={[UserRole.AUTHORIZER, UserRole.ADMIN]}>
            <Box sx={{ display: "flex", flexDirection: "column"}}>
                <ApacViewProvider>
                    <AuthorizationProvider>
                        <AutorizeMultiplesApacProvider>
                            <ApacFilter/>
                            <ApacTable/>
                        </AutorizeMultiplesApacProvider>
                    </AuthorizationProvider>
                </ApacViewProvider>
            </Box>
        </RouteGuard>
    )
}