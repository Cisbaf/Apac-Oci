import { Box } from "@mui/material";
import IdentifyEstablishmentForm from "./identifyEstablishmentForm";
import IdentifyMainProcedure from "./identifyMainProcedureForm";
import IdentifyPatientForm from "./identifyPatientForm";
import IdentifySubProcedures from "./identifySubProceduresForm";
import IdentifyCidForm from "./identifyCidForm";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";
import { useRouter } from "next/navigation";
import { useFormRequest } from "../../contexts/FormApacRequest";
import ConfirmButton from "@/shared/components/ConfirmButton";
import { adapterFormSubProcedures, formatDateToISO } from "../../utils/adapterForm";
import { ToSnakeCase } from "@/shared/utils/snakeCase";
import IdentifyMedicAuthorizingForm from "./indentifyMedicAuthorizingForm";
import IdentifyMedicSupervisingForm from "./identifyMedicSupervisingForm";
import React from "react";
import IdentifyRequestDate from "./identifyRequestDate";


export default function ApacRequestFinishForm() {
    const { form } = useFormRequest();
    const { getValues } = form;
    const { showResponseApi, showBackdrop } = useGlobalComponents();
    const route = useRouter();

    const finish = async() => {
        showBackdrop(true, "Solicitando apac!");
        const data = structuredClone(getValues());

        // @ts-expect-error adapterFormSubProcedures converte para o formato snake_case esperado pela API, incompatível com o tipo do form
        data.apacData.subProcedures = adapterFormSubProcedures(data.apacData.subProcedures);
        data.apacData.procedureDate = formatDateToISO(data.apacData.procedureDate);
        data.apacData.dischargeDate = formatDateToISO(data.apacData.dischargeDate);
        data.apacData.patientBirthDate = formatDateToISO(data.apacData.patientBirthDate);
        // @ts-expect-error campo é string no form, mas aceita null para "sem diagnóstico" no envio à API
        data.apacData.diagnosticDate = data.apacData.diagnosticDate? data.apacData.diagnosticDate : null
        // data.apacData.diagnosticDate = formatDateToISO(data.apacData.diagnosticDate);
        const data_json = JSON.stringify(ToSnakeCase(data));
        const response = await fetch('/api/proxy/apac_request/api', {
            method: "POST",
            body: data_json
        })
        const response_json = await showResponseApi(response);
        setTimeout(()=>{
            if (response.ok) {
                route.push("/visualizar?id=" + response_json.apac_request_id);
            }
            showBackdrop(false)
        }, 500);
    }

    return(
        <Box sx={{
            display: "flex",
            flexDirection: "column",
            gap: 2
        }}>
            <IdentifyRequestDate disabled/>
            <IdentifyEstablishmentForm disabled/>
            <IdentifyPatientForm disabled/>
            <IdentifyMainProcedure disabled/>
            <IdentifySubProcedures disabled/>
            <IdentifyCidForm disabled/>
            <IdentifyMedicSupervisingForm disabled/>
            <IdentifyMedicAuthorizingForm disabled/>
            <br></br>
            <ConfirmButton
                holdDuration={750}
                confirmedColor="green"
                progressColor="green"
                baseColor="#acffa3"
                onConfirm={finish}>
                Finalizar
            </ConfirmButton>
        </Box>
    )
}