import React from 'react';
import { Box, Button } from '@mui/material';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ApacRequestService from '@/app/solicitar/apacRequest/components/ApacRequestService';
import IdentifyEstablishmentForm from '@/app/solicitar/apacRequest/components/forms/identifyEstablishmentForm';
import IdentifyPatientForm from '@/app/solicitar/apacRequest/components/forms/identifyPatientForm';
import IdentifyMainProcedure from '@/app/solicitar/apacRequest/components/forms/identifyMainProcedureForm';
import IdentifySubProcedures from '@/app/solicitar/apacRequest/components/forms/identifySubProceduresForm';
import IdentifyCidForm from '../components/forms/identifyCidForm';
import IdentifyMedicForm from '../components/forms/identifyMedicSupervisingForm';
import ApacRequestDataDisabled from '../components/forms/finishFormApacRequest';
import { fakeRequestForm } from '../utils/dataFakes';
import { DataApacRequest } from '../contexts/ApacRequestContext';
import { fakeDataApacRequest } from '../utils/dataFakes';
import { RequestForm } from '../schemas/requestForm';
import { FormResponse } from '@/shared/repositories/formRepository';
import { GlobalComponentsProvider } from '@/shared/context/GlobalUIContext';
import { useFormRequest } from '../contexts/FormApacRequest';

const Finish: React.FC = () => {
    const { handleComplete, form } = useFormRequest();

    return (
    <Button
        variant='contained'
        onClick={() => handleComplete && handleComplete(form.getValues())}
    >
        Enviar
    </Button>
    );
};

test("Apac Request Service", async () => {
    let finish;

    const fakePromise = (): Promise<DataApacRequest> => {
        return Promise.resolve(fakeDataApacRequest);
    };

    const handleComplete = (data: RequestForm): Promise<FormResponse> => {
        finish = data;
        return Promise.resolve({ success: true, message: "" });
    };

    await waitFor(() =>
        render(
            <GlobalComponentsProvider>
                <ApacRequestService
                    initialData={fakeRequestForm}
                    handleComplete={handleComplete}
                    getDataRequest={fakePromise}>
                    <Box>
                        <IdentifyEstablishmentForm />
                        <IdentifyPatientForm />
                        <IdentifyMainProcedure />
                        <IdentifySubProcedures />
                        <IdentifyCidForm />
                        <IdentifyMedicForm />
                        <Finish/>
                    </Box>
                </ApacRequestService>
            </GlobalComponentsProvider>
        )
    );

    const button = await waitFor(() =>
        screen.getByRole('button', { name: /Enviar/i })
    );
    fireEvent.click(button);

    expect(finish).toEqual(fakeRequestForm);

});
