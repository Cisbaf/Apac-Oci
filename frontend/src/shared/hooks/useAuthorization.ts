// hooks/useAuthorization.ts
import { UserRole } from "@/shared/schemas/user";
import { useContextUser } from "../context/UserContext";

export const useAuthorization = (allowedRoles: UserRole[]) => {
  const user = useContextUser();
  
  const isAuthorized = allowedRoles.includes(user.role);
  const isUnauthorized = !allowedRoles.includes(user.role);
  
  return { isAuthorized, isUnauthorized };
};