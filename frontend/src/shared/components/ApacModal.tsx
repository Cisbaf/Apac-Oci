import CustomModal, {ModalHandles} from "@/shared/components/Modal";
import { ApacRequest } from "@/app/solicitar/apacRequest/schemas/apacRequest";
import { Box } from "@mui/material";
import IdentifyEstablishmentForm from '@/app/solicitar/apacRequest/components/forms/identifyEstablishmentForm';
import IdentifyPatientForm from '@/app/solicitar/apacRequest/components/forms/identifyPatientForm';
import IdentifyMainProcedure from '@/app/solicitar/apacRequest/components/forms/identifyMainProcedureForm';
import IdentifySubProcedures from '@/app/solicitar/apacRequest/components/forms/identifySubProceduresForm';
import IdentifyMedicForm from '@/app/solicitar/apacRequest/components/forms/identifyMedicForm';
import { ApacRequestFormProvider } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { ApacRequestFillingData } from "@/app/solicitar/apacRequest/contexts/ApacRequestContext";
import { DataApacRequest } from '@/app/solicitar/apacRequest/contexts/ApacRequestContext';
import { RequestForm } from "@/app/solicitar/apacRequest/schemas/requestForm";
import { convertApacDataToForm } from "@/app/solicitar/apacRequest/utils/convertApacData";

interface ApacModalProps {
    apacRequest: ApacRequest;
    ref: React.RefObject<ModalHandles | null>;
    onClose: ()=> void;
}

export default function ApacModal({ apacRequest, ref, onClose }: ApacModalProps) {
    
    const dataRequest: DataApacRequest = {
        establishments: [apacRequest?.establishment],
        procedures: [apacRequest?.apac_data.main_procedure]
    } 
    const dataForm: RequestForm = {
        requesterId: apacRequest.requester.id,
        establishmentId: apacRequest.establishment.id,
        apacData: convertApacDataToForm(apacRequest.apac_data)
    }

    
    return (
        <CustomModal 
            title={apacRequest?.apac_data.main_procedure.name} 
            ref={ref}
            handleChanged={(open)=>{
                if (!open) onClose();
            }}>
   
             <ApacRequestFillingData dataRequest={dataRequest}>
                <ApacRequestFormProvider initialData={dataForm} disabled>
                <Box sx={{
                    display: "flex",
                    flexDirection: "column",
                    maxHeight: "80vh",
                    overflow: "auto",
                    paddingTop: 5,
                    gap: 2,
                    }}>
                    <IdentifyEstablishmentForm/>
                    <IdentifyPatientForm/>
                    <IdentifyMainProcedure/>
                    <IdentifySubProcedures/>
                    <IdentifyMedicForm/>
                </Box>
                
                </ApacRequestFormProvider>
            </ApacRequestFillingData>
     
        </CustomModal>
    )
}