import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { GlobalComponentsProvider } from '@/shared/context/GlobalUIContext';
import { RequestForm } from '../schemas/requestForm';

const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
    useRouter: () => ({ push: mockPush }),
    usePathname: () => '/solicitar',
}));

const mockGetValues = jest.fn();
jest.mock('@/app/solicitar/apacRequest/contexts/FormApacRequest', () => ({
    useFormRequest: () => ({ form: { getValues: mockGetValues } }),
}));

// As subforms (renderizadas em modo `disabled` só para exibição) dependem de
// contextos que não são o alvo deste teste (`useRequestData`, CADSUS etc.) —
// substituídas por stubs para isolar a lógica de submissão do FinishForm.
jest.mock('../components/forms/identifyEstablishmentForm', () => function StubEstablishment() { return <div>Estabelecimento</div>; });
jest.mock('../components/forms/identifyPatientForm', () => function StubPatient() { return <div>Paciente</div>; });
jest.mock('../components/forms/identifyMainProcedureForm', () => function StubMainProcedure() { return <div>Procedimento Principal</div>; });
jest.mock('../components/forms/identifySubProceduresForm', () => function StubSubProcedures() { return <div>Subprocedimentos</div>; });
jest.mock('../components/forms/identifyCidForm', () => function StubCid() { return <div>CID</div>; });
jest.mock('../components/forms/identifyMedicSupervisingForm', () => function StubMedicSupervising() { return <div>Médico Supervisor</div>; });
jest.mock('../components/forms/indentifyMedicAuthorizingForm', () => function StubMedicAuthorizing() { return <div>Médico Autorizador</div>; });
jest.mock('../components/forms/identifyRequestDate', () => function StubRequestDate() { return <div>Data da Solicitação</div>; });

// ConfirmButton exige "pressione e segure"; não é o alvo deste teste, então
// vira um botão comum que dispara onConfirm no clique.
jest.mock('@/shared/components/ConfirmButton', () => ({
    __esModule: true,
    default: function StubConfirmButton({ onConfirm, children }: { onConfirm: () => void; children: React.ReactNode }) {
        return <button onClick={onConfirm}>{children}</button>;
    },
}));

import ApacRequestFinishForm from '../components/forms/finishFormApacRequest';

const validFormValues: RequestForm = {
    requesterId: 1,
    establishmentId: 2,
    requestDate: '01/07/2026',
    apacData: {
        patientName: 'PACIENTE TESTE',
        patientRecordNumber: '121212',
        patientCns: '701805209274077',
        patientCpf: '18714933748',
        patientBirthDate: '12/03/1999',
        patientRaceColor: '01',
        patientGender: 'M',
        patientMotherName: 'MAE TESTE',
        patientAddressStreetType: '081',
        patientAddressStreetName: 'RUA TESTE',
        patientAddressNumber: '200',
        patientAddressComplement: '',
        patientAddressPostalCode: '22221036',
        patientAddressNeighborhood: 'BAIRRO TESTE',
        patientAddressCity: 'Rio de Janeiro',
        patientAddressState: 'RJ',
        supervisingPhysicianName: 'MEDICO SUPERVISOR',
        supervisingPhysicianCns: '706000343458946',
        supervisingPhysicianCbo: '78956',
        authorizingPhysicianName: 'MEDICO AUTORIZADOR',
        authorizingPhysicianCns: '705804481243730',
        authorizingPhysicianCbo: '79654',
        cidId: 6,
        procedureDate: '01/08/2026',
        dischargeDate: '02/08/2026',
        diagnosticDate: '01/08/2026',
        mainProcedureId: 231,
        subProcedures: [
            {
                procedure: { id: 10, name: 'Subprocedimento', code: '0101' } as never,
                quantity: 1,
                cbo: '78956',
                cnes: '1234567',
                checked: true,
            },
        ],
    },
};

function renderFinishForm() {
    render(
        <GlobalComponentsProvider>
            <ApacRequestFinishForm />
        </GlobalComponentsProvider>
    );
}

function clickFinish() {
    fireEvent.click(screen.getByText('Finalizar'));
}

beforeEach(() => {
    jest.clearAllMocks();
    mockGetValues.mockReturnValue(validFormValues);
    global.fetch = jest.fn();
});

test('submissão com sucesso envia os dados adaptados e redireciona para /visualizar', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ apac_request_id: 42, message: 'APAC solicitada com sucesso' }),
    });

    renderFinishForm();
    clickFinish();

    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));

    const [url, options] = (global.fetch as jest.Mock).mock.calls[0];
    expect(url).toBe('/api/proxy/apac_request/api');
    const body = JSON.parse(options.body);

    // Datas convertidas de dd/mm/yyyy (form) para yyyy-mm-dd (API).
    expect(body.apac_data.procedure_date).toBe('2026-08-01');
    expect(body.apac_data.discharge_date).toBe('2026-08-02');
    // diagnostic_date NÃO passa por formatDateToISO (linha comentada no
    // código-fonte) — vai cru, em dd/mm/yyyy, diferente dos outros 3 campos
    // de data. Comportamento real caracterizado aqui; achado registrado
    // como T-033 (provável bug), não corrigido nesta tarefa.
    expect(body.apac_data.diagnostic_date).toBe('01/08/2026');
    // Subprocedimentos adaptados para o formato snake_case esperado pela API,
    // só os marcados (`checked: true`).
    expect(body.apac_data.sub_procedures).toEqual([
        { procedure_id: 10, quantity: 1, cbo: '78956', cnes: '1234567' },
    ]);

    await waitFor(() => expect(mockPush).toHaveBeenCalledWith('/visualizar?id=42'), { timeout: 1000 });
});

test('falha da API não redireciona e mostra o erro', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: () => Promise.resolve({ message: 'CPF do paciente inválido' }),
    });

    renderFinishForm();
    clickFinish();

    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));
    expect(await screen.findByText('CPF do paciente inválido')).toBeInTheDocument();

    // Dá tempo pro `setTimeout` de 500ms do handler rodar; push não deve
    // acontecer nesse caminho.
    await new Promise((resolve) => setTimeout(resolve, 600));
    expect(mockPush).not.toHaveBeenCalled();
});

test('diagnosticDate vazio é enviado como null, não como string formatada', async () => {
    mockGetValues.mockReturnValue({
        ...validFormValues,
        apacData: { ...validFormValues.apacData, diagnosticDate: '' },
    });
    (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ apac_request_id: 7, message: 'ok' }),
    });

    renderFinishForm();
    clickFinish();

    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));
    const [, options] = (global.fetch as jest.Mock).mock.calls[0];
    const body = JSON.parse(options.body);
    expect(body.apac_data.diagnostic_date).toBeNull();
});
