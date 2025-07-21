// components/SkeletonLayout.tsx
"use client";
import React from "react";
import { Skeleton, Stack } from "@mui/material";

export default function SkeletonLayout() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <div
        style={{
          width: 270,
          backgroundColor: "#2f3b46",
          color: "#fff",
          padding: 16,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Skeleton variant="rectangular" width="100%" height={50} style={{ marginBottom: 2, backgroundColor: "#455a64" }} />
        <Skeleton variant="rectangular" width="100%" height={40} style={{ marginBottom: 10, backgroundColor: "#455a64" }} />
        <Skeleton variant="circular" width={50} height={50} style={{ marginBottom: 16, backgroundColor: "#455a64" }} />
        <Skeleton width="60%" height={20} style={{ marginBottom: 32, backgroundColor: "#455a64" }} />

        <Stack spacing={2}>
          <Skeleton variant="rectangular" width="100%" height={30} style={{ backgroundColor: "#455a64" }} />
          <Skeleton variant="rectangular" width="100%" height={30} style={{ backgroundColor: "#455a64" }} />
          <Skeleton variant="rectangular" width="100%" height={30} style={{ backgroundColor: "#455a64" }} />
        </Stack>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, padding: 32, backgroundColor: "#f7f7f7" }}>
        {/* Header */}
        <Skeleton width="30%" height={40} style={{ marginBottom: 24 }} />

        {/* Card Filter */}
        <div
          style={{
            backgroundColor: "#fff",
            padding: 24,
            marginLeft: 24,
            borderRadius: 8,
            boxShadow: "0px 1px 3px rgba(0,0,0,0.1)",
          }}
        >
          <div style={{ display: "flex", gap: 16, alignItems: "center", flexWrap: "wrap" }}>
            <div>
              <Skeleton width={100} height={20} style={{ marginBottom: 8 }} />
              <Skeleton variant="rectangular" width={140} height={36} />
            </div>
            <div>
              <Skeleton width={100} height={20} style={{ marginBottom: 8 }} />
              <Skeleton variant="rectangular" width={140} height={36} />
            </div>
            <div>
              <Skeleton width={80} height={20} style={{ marginBottom: 8 }} />
              <Skeleton variant="rectangular" width={140} height={36} />
            </div>
            <div style={{ marginTop: 24 }}>
              <Skeleton variant="rectangular" width={100} height={36} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
