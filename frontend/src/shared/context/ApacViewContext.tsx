import React from "react";
import { ApacRequest } from "@/app/solicitar/apacRequest/schemas/apacRequest";
import { useGlobalComponents } from "./GlobalUIContext";

interface ApacViewType {
    listApac: ApacRequest[];
    searchApacs: (params: string) => Promise<void>;
    removeApac: (apac: ApacRequest) => void;
}


const ApacViewContext = React.createContext<ApacViewType | null>(null);


interface ApacViewProps {
    children: React.ReactNode;
}

export default function ApacViewProvider({children}: ApacViewProps) {
    const [listApac, setList] = React.useState<ApacRequest[]>([]);
    const { showResponseApi, showBackdrop } = useGlobalComponents();

    const searchApacs = async(params: string) => {
        showBackdrop(true, "Buscando...");
        setList([]);
        const response = await fetch(`/api/proxy/apac_request/api?${params}`);
        const response_json = await showResponseApi(response);
        if (response.ok) {
            setList(response_json.data);
        }
        showBackdrop(false);
    }

    const removeApac = (apac: ApacRequest) => {
        setList(listApac.filter(obj=>obj.id != apac.id));
    }

    return (
        <ApacViewContext.Provider value={{
            listApac,
            searchApacs,
            removeApac
            }}>
            {children}
        </ApacViewContext.Provider>
    )
}


export function useApacViewContext() {
  const context = React.useContext(ApacViewContext)
  if (!context) {
    throw new Error('xac must be used within a x')
  }
  return context
}