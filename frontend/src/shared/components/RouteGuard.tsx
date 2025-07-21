// components/RouteGuard.tsx
'use client'
import React from "react";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";
import { useRouter } from "next/navigation";
import { useAuthorization } from "@/shared/hooks/useAuthorization";
import { UserRole } from "../schemas/user";

interface RouteGuardProps {
  allowedRoles: UserRole[];
  children: React.ReactNode;
  redirectTo?: string;
  message?: string;
}

export const RouteGuard = ({
  allowedRoles,
  children,
  redirectTo = "/",
  message = "Não Autorizado!"
}: RouteGuardProps) => {
  const { showAlert } = useGlobalComponents();
  const { isUnauthorized } = useAuthorization(allowedRoles);
  const route =  useRouter();

  React.useEffect(() => {
    if (isUnauthorized) {
      showAlert({ message: message, color: "error" });
      route.push(redirectTo);
    }
  }, [isUnauthorized]);

  return <>{children}</>;
};