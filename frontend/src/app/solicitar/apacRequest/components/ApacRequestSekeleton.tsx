import React from "react";
import { Box, Skeleton } from "@mui/material";


export default function ApacRequestSkeleton() {
    return(
        <Box
            width="100%"
            display="flex"
            flexDirection="column"
            gap={2}>
            <Skeleton variant="rectangular" height={50} />
            <Skeleton variant="rectangular" height={100} />
            <Skeleton variant="rectangular" height={400} />
            <Skeleton variant="rectangular" height={200} />
            <Skeleton variant="rectangular" height={50} />
        </Box>
    )
}