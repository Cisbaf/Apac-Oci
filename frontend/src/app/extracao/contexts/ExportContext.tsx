import React from "react";
import useExtractForm from "../hooks/useExtractForm";
import useBatchsList from "../hooks/useBatchList";
import GetExtractFile from "../controllers/GetExtractFile";
import { GenerateStringToDownloadFile } from "../controllers/Downloads";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";

interface ExportContextType {
    hookExtractForm: ReturnType<typeof useExtractForm>;
    hookBatchsList: ReturnType<typeof useBatchsList>;
    extract: ()=> void;
}

interface ExportContextProps {
    children: any;
}

const ExportContext = React.createContext<ExportContextType | null>(null);

export function ExportContextProvider({ children }: ExportContextProps) {

    const hookExtractForm = useExtractForm();
    const hookBatchsList = useBatchsList();
    const { showAlert, showBackdrop} = useGlobalComponents();

    const extract = async() => {
        showBackdrop(true, "Extraindo Apac's...");
        const form = hookExtractForm.getValues();
        try {
            const response = await GetExtractFile(form);
            if (response.content) {
                var fileName;
                const extension = form.production.toLocaleString("pt-BR", { month: "short" }).toUpperCase();
                const establishmentShortName = form.establishmentName;
                if (!extension || !establishmentShortName) {
                    fileName = "exportacao.txt";
                } else {
                    fileName = `AP${establishmentShortName}.${extension}`;
                }
                GenerateStringToDownloadFile(fileName, response.content);
            } else {
                throw new Error("Problema ao extrair, contate o desenvolvedor!")
            }
        } catch (e) {
            showAlert({color: "error", message: "Erro ao extrair!>" + String(e)});
        } finally {
            showBackdrop(false);
        }
    }

    return (
        <ExportContext.Provider value={{
            hookBatchsList,
            hookExtractForm,
            extract
        }}>
            {children}
        </ExportContext.Provider>
    );
}

export function useExportContext(): ExportContextType {
    const context = React.useContext(ExportContext);
    if (!context) {
        throw new Error("...");
    }
    return context;
}