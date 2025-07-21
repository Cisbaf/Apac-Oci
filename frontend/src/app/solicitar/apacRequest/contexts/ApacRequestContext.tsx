// context/UserContext.tsx
import React from "react";
import { Procedure, Establishment } from "@/shared/schemas";

export interface DataApacRequest {
  procedures: Procedure[];
  establishments: Establishment[];
}

const ApacRequestFillingDataContext = React.createContext<DataApacRequest | null>(null);

interface ApacRequestContextProps {
  dataRequest: DataApacRequest;
  children: React.ReactNode;
}

export function ApacRequestFillingData({ dataRequest, children }: ApacRequestContextProps) {
  const { procedures, establishments } = dataRequest;

  return (
    <ApacRequestFillingDataContext.Provider value={{ procedures, establishments }}>
      {children}
    </ApacRequestFillingDataContext.Provider>
  );
}

export function useRequestData(): DataApacRequest {
    const context = React.useContext(ApacRequestFillingDataContext);
    if (!context) {
      throw new Error("useRequestForm must be used within a RequestFormProvider");
    }
  return context;
}