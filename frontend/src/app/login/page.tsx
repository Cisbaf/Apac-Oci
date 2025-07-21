'use client';
import React from "react";
import Login from "@/shared/components/Login";

export default function LoginPage() {
  return (
    <React.Suspense fallback={<div>Carregando...</div>}>
      <Login />
    </React.Suspense>
  );

}