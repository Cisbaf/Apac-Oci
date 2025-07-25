import { Box, Typography, Button } from "@mui/material";
import IdentifyEstablishmentForm from "./identifyEstablishmentForm";
import IdentifyMainProcedure from "./identifyMainProcedureForm";
import IdentifyMedicForm from "./identifyMedicForm";
import IdentifyPatientForm from "./identifyPatientForm";
import IdentifySubProcedures from "./identifySubProceduresForm";
import IdentifyCidForm from "./identifyCidForm";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";
import { useRouter } from "next/navigation";
import { useFormRequest } from "../../contexts/FormApacRequest";
import ConfirmButton from "@/shared/components/ConfirmButton";
import { adapterFormSubProcedures } from "../../utils/adapterForm";
import { ToSnakeCase } from "@/shared/utils/snakeCase";

export default function ApacRequestFinishForm() {
    const { form } = useFormRequest();
    const { getValues } = form;
    const { showResponseApi, showBackdrop } = useGlobalComponents();
    const route = useRouter();

    const finish = async() => {
        showBackdrop(true, "Solicitando apac!");
        const data = structuredClone(getValues());
        // @ts-ignore
        data.apacData.subProcedures =  adapterFormSubProcedures(data.apacData.subProcedures);
        const data_json = JSON.stringify(ToSnakeCase(data))
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
            <IdentifyEstablishmentForm disabled/>
            <IdentifyPatientForm disabled/>
            <IdentifyMainProcedure disabled/>
            <IdentifySubProcedures disabled/>
            <IdentifyCidForm disabled/>
            <IdentifyMedicForm disabled/>
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