import React from "react";
import { Typography, Box } from "@mui/material";

interface TextModeProps {
    title: string;
    value: string;
    children: React.ReactNode
}

export default function TextMode({title, value, children}: TextModeProps) {
    return (
        <>
        {title?
        <Box>
            <Typography variant="h6">{title}</Typography>
            <Typography variant="body1">{value}</Typography>
        </Box>:
        {children}
        }
        </>
    )
}