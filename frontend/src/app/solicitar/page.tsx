'use client'
import React from 'react';
import { Typography, Box, Divider } from '@mui/material';
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import { ApacRequestFormProvider } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { ApacRequestFillingData, DataApacRequest } from '@/app/solicitar/apacRequest/contexts/ApacRequestContext';
import { ApacRequestFetchApi } from '@/app/solicitar/apacRequest/services/ApacRequestApi';
import { fakeDataRequestFillingPart } from '@/app/solicitar/apacRequest/utils/dataFakes';
import IdentifyEstablishmentForm from '@/app/solicitar/apacRequest/components/forms/identifyEstablishmentForm';
import IdentifyPatientForm from '@/app/solicitar/apacRequest/components/forms/identifyPatientForm';
import IdentifyMainProcedure from '@/app/solicitar/apacRequest/components/forms/identifyMainProcedureForm';
import IdentifySubProcedures from '@/app/solicitar/apacRequest/components/forms/identifySubProceduresForm';
import IdentifyCidForm from '@/app/solicitar/apacRequest/components/forms/identifyCidForm';
import IdentifyMedicSupervisingForm from '@/app/solicitar/apacRequest/components/forms/identifyMedicSupervisingForm';
import IdentifyMedicAuthorizingForm from './apacRequest/components/forms/indentifyMedicAuthorizingForm';
import ApacRequestFinishForm from '@/app/solicitar/apacRequest/components/forms/finishFormApacRequest';
import ApacRequestSkeleton from '@/app/solicitar/apacRequest/components/ApacRequestSekeleton';
import { RouteGuard } from "@/shared/components/RouteGuard";
import { UserRole } from "@/shared/schemas/user";
import StepForm from '@/shared/components/StepComponent';
import { ProgressStepper } from "@/shared/components/ProgressStepper";
import { emptyRequestForm } from './apacRequest/utils/formDataApacRequest';


export default function PageApacRequest() {
    const [data, setData] = React.useState<DataApacRequest>();

    React.useEffect(()=>{
        ApacRequestFetchApi()
        .then(data=>setData(data))
    }, [])

    return(
       <Box sx={{ display: "flex", flexDirection: "column"}}>
            <Box sx={{ display: "flex", alignItems: "center", gap: 4}}>
                <AppRegistrationIcon sx={{fontSize: 32}}/>
                <Typography variant='h6'>Solicitar Apac Oci</Typography>
            </Box>
            <Divider sx={{mt: 1, mb: 2}}/>
            {data? 
            <ApacRequestFillingData
                dataRequest={data}>
                <RouteGuard
                    allowedRoles={[UserRole.REQUESTER, UserRole.ADMIN]}>
                    <ApacRequestFormProvider
                        initialData={emptyRequestForm}>
                        <ProgressStepper>
                            <StepForm>
                                <IdentifyEstablishmentForm/>
                                <IdentifyPatientForm/>
                            </StepForm>
                            <StepForm>
                                <IdentifyMainProcedure/>
                                <IdentifySubProcedures/>
                            </StepForm>
                            <StepForm>
                                <IdentifyCidForm/>
                                <IdentifyMedicSupervisingForm/>
                                <IdentifyMedicAuthorizingForm/>
                            </StepForm>
                            <StepForm>
                                <ApacRequestFinishForm/>
                            </StepForm>
                        </ProgressStepper>
                    </ApacRequestFormProvider>
                </RouteGuard>
            </ApacRequestFillingData>
            : <ApacRequestSkeleton/>
            }
        </Box>
    )
}