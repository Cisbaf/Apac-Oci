"use client";
import React from "react";
import ApacFilter from "@/shared/components/ApacFilter";
import ApacTable from "@/shared/components/ApacTable";
import ApacViewProvider from "@/shared/context/ApacViewContext";
import { AuthorizationProvider } from "../responder/apacAuthorization/context/authorizationContext";
import { Box, Typography, Divider } from "@mui/material";
import { PlaylistAddCheck } from "@mui/icons-material";

export default function ApacViewPage() {
    return(
         <Box sx={{ display: "flex", flexDirection: "column", width: "100%", overflow: "auto"}}>
            <ApacViewProvider>
                <AuthorizationProvider>
                    <ApacFilter/>
                    <ApacTable onlyView/>
                </AuthorizationProvider>
            </ApacViewProvider>
        </Box>
      
    )
}