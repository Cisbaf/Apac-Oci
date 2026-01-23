import React, { createContext, useContext } from "react";
import { useForm, UseFormReturn, useWatch, useFieldArray } from "react-hook-form";
import { RequestForm } from "../schemas/requestForm";
import { useRequestData } from "./ApacRequestContext";
import { useContextUser } from "@/shared/context/UserContext";

interface RequestFormType {
  form: UseFormReturn<RequestForm, any, RequestForm>;
  disabled?: boolean; // Adiciona a propriedade disabled
  textMode?: boolean;
}

export const ApacRequestFormContext = createContext<RequestFormType | null>(null);

export function ApacRequestFormProvider({
  initialData,
  children,
  disabled = false, // Adiciona o prop disabled com valor padrão false
  textMode = false
}: {
  initialData: RequestForm;
  children: React.ReactNode;
  disabled?: boolean; // Tipagem para o prop disabled
  textMode?: boolean;
}) {
  const form = useForm<RequestForm>({
    defaultValues: initialData,
  });
  const user = useContextUser();
  const { control, setValue } = form;
  setValue("requesterId", user.id)
  const { procedures } = useRequestData();
  const prevMainProcedureId = React.useRef<number>(initialData.apacData.mainProcedureId);
  const mainProcedureField = useWatch({
      control,
      name: "apacData.mainProcedureId"
  });

 const { append } = useFieldArray({
      control,
      name: "apacData.subProcedures",
  });

  

  React.useEffect(()=>{
    const procedure = procedures.find(p=>p.id === mainProcedureField);

    if (!procedure) return;

    const currentId = procedure.id;

    if (prevMainProcedureId.current !== currentId && !disabled) {
        prevMainProcedureId.current = currentId;
        setValue("apacData.cidId", 0);
        setValue("apacData.subProcedures", []);
        // Filtra e adiciona apenas os filhos do novo mainProcedure
        procedure.children?.forEach(p=>{
            append({
                procedure: p,
                quantity: 0,
                cbo: "",
                cnes: "",
                checked: false
            });
        })
    }

  }, [mainProcedureField]);


  React.useEffect(()=>{
    if (disabled && initialData) {

      initialData.apacData.subProcedures.forEach((procedure, i)=>{
        if (procedure.checked && procedure.cbo || procedure.cnes ) {
          setValue(`apacData.subProcedures.${i}.useThirdPartyData`, true);
          setValue(`apacData.subProcedures.${i}.cbo`, procedure.cbo);
          setValue(`apacData.subProcedures.${i}.cnes`, procedure.cnes);
        }
      })
    }
  }, [])

  return (
    <ApacRequestFormContext.Provider value={{ form, disabled, textMode }}>
      {children}
    </ApacRequestFormContext.Provider>
  );
}

export function useFormRequest(): RequestFormType {
  const context = useContext(ApacRequestFormContext);
  if (!context) {
    throw new Error("useRequestForm must be used within a RequestFormProvider");
  }
  return context;
}