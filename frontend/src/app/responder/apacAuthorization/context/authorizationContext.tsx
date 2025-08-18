import React from "react";
import { ApacRequest } from "@/app/solicitar/apacRequest/schemas/apacRequest";
import CustomModal, {ModalHandles} from "@/shared/components/Modal";
import { Box, Divider, Typography, TextField } from "@mui/material";
import { useApacViewContext } from "@/shared/context/ApacViewContext";
import ConfirmButton from "@/shared/components/ConfirmButton";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";
import { useContextUser } from "@/shared/context/UserContext";
import { formatDateBr } from "@/app/solicitar/apacRequest/utils/adapterForm";

interface AuthorizationType {
    authorize: (id: number, status: "approved"|"reject"|null) => void;
}

const AuthorizationContext = React.createContext<AuthorizationType | null>(null);

export function AuthorizationProvider({children}: {children: React.ReactNode}) {
    const { listApac, removeApac } = useApacViewContext();
    const { showBackdrop, showAlert, showResponseApi } = useGlobalComponents();
    const [apacRequest, setApacRequest] = React.useState<ApacRequest>();
    const [status, setStatus] = React.useState<"approved"|"reject"|null>(null);
    const modalRef = React.useRef<ModalHandles>(null);
    const [justification, setJustification] = React.useState("");
    const user = useContextUser();
    const infoApproved = {
        "Nome:": apacRequest?.apac_data.patient_data.name,
        "Data de Solicitação do Procedimento:": formatDateBr(apacRequest?.apac_data.procedure_date || ""),
        "Procedimento:": apacRequest?.apac_data.main_procedure.name
    }

    React.useEffect(()=> {
        if(status) modalRef.current?.openModal();
    }, [status])
    
    const authorizate = async(data: {body: string, endpoint: string}) => {
        if (!apacRequest || !modalRef.current) return;
        showBackdrop(true, "Solicitando...")
        const response = await fetch(`/api/proxy/apac_request/${data.endpoint}`, {
            method: "POST",
            body: data.body
        });
        await showResponseApi(response);
        showBackdrop(false);
        if (!response.ok) return;
        removeApac(apacRequest);
        modalRef.current.closeModal()
    }

    const approved = async() => {
        if (!user || !apacRequest) return;
        authorizate({
            body: JSON.stringify({
                apac_request_id: apacRequest.id,
                authorizer_id: user.id
            }),
            endpoint: "approved"
        });
    }

    const reject = async() => {
        if (!user || !apacRequest) return;
        authorizate({
            body: JSON.stringify({
                apac_request_id: apacRequest.id,
                authorizer_id: user.id,
                justification: justification
            }),
            endpoint: "reject"
        });
    }

    return (
        <AuthorizationContext.Provider value={{
            authorize(id, status) {
                setApacRequest(listApac.find(obj=>obj.id === id));
                setStatus(status);
            }
        }}>
        {children}
        <CustomModal
            ref={modalRef}
            title={status === "approved"? "Aprovar Solicitação" : "Negar Solicitação"}
            handleChanged={(open)=>{
            if (open) return;
            setApacRequest(undefined);
            setStatus(null); 
            setJustification("");
        }}>
            <Box>
                <br></br>
                <Divider/>
                <br></br>
                {status === "approved" && <>
                    <Box sx={{
                        display: "flex",
                        gap: 0.5,
                        flexDirection: "row"
                    }}>
                        <Typography sx={{textWrap: "nowrap"}}>Tem certeza que deseja</Typography>
                        <Typography sx={{textWrap: "nowrap"}} color="success">APROVAR</Typography>
                        <Typography sx={{textWrap: "nowrap"}}>esta Solicitação de APAC OCI para o paciente abaixo?</Typography>
                    </Box>
                    <br></br>
                    {Object.entries(infoApproved).map((obj, i)=>(
                        <Box key={`box-info-${i}`} sx={{
                            display: "flex",
                            gap: 0.5,
                            alignItems: "center",
                            flexDirection: "row"
                        }}>
                            <Typography variant="h6" key={`box-info-t1-${i}`} >{obj[0]}</Typography>
                            <Typography key={`box-info-t2-${i}`}>{obj[1]}</Typography>
                        </Box>
                    ))}
                    <br></br>
                    <hr></hr>
                    <br></br>
                    <ConfirmButton
                        holdDuration={750}
                        confirmedColor="#155724"
                        progressColor="#155724"
                        baseColor="#d4edda"
                        onConfirm={approved}>APROVAR SOLICITAÇÃO</ConfirmButton>
                </>}
                {status === "reject" &&<>
                    {Object.entries(infoApproved).map((obj, i)=>(
                        <Box key={`box-info-${i}`} sx={{
                            display: "flex",
                            gap: 0.5,
                            alignItems: "center",
                            flexDirection: "row"
                        }}>
                            <Typography variant="h6" key={`box-info-t1-${i}`} >{obj[0]}</Typography>
                            <Typography key={`box-info-t2-${i}`}>{obj[1]}</Typography>
                        </Box>
                    ))}
                    <br></br>
                    <hr></hr>
                    <br></br>
                    <Box sx={{
                        display: "flex",
                        gap: 0.5,
                        flexDirection: "row"
                    }}>
                        <Typography sx={{textWrap: "nowrap"}}>Para</Typography>
                        <Typography sx={{textWrap: "nowrap"}} color="error">NEGAR</Typography>
                        <Typography sx={{textWrap: "nowrap"}}>esta solicitação, preencha uma justificativa.</Typography>
                    </Box>
                    <br></br>
                        <TextField
                        id="outlined-multiline-static"
                        label="Justificativa"
                        value={justification}
                        onChange={(e) => setJustification(e.target.value)}
                        fullWidth
                        multiline
                        rows={6}
                        sx={{
                            '& .MuiInputBase-inputMultiline': {
                            resize: 'both', // pode ser 'vertical' se quiser só na altura
                            overflow: 'auto'
                            }
                        }}
                        />
                    <br></br>
                    <br></br>
                    <hr></hr>
                    <br></br>
                     <ConfirmButton
                        holdDuration={750}
                        confirmedColor="#721c24"
                        progressColor="#721c24"
                        baseColor="#f8d7da"
                        onConfirm={reject}>Negar Solicitação</ConfirmButton>
                </>}
            </Box>
        </CustomModal>
        </AuthorizationContext.Provider>
    )
}

export function useApacAuthorizationContext() {
  const context = React.useContext(AuthorizationContext)
  if (!context) {
    throw new Error('x must be used within a x')
  }
  return context
}