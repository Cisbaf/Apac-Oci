import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { GlobalComponentsProvider } from '@/shared/context/GlobalUIContext';
import StepForm from '@/shared/components/StepComponent';
import { FormRepository, FormProps } from '@/shared/repositories/formRepository';

const mockGetValues = jest.fn();

jest.mock('@/app/solicitar/apacRequest/contexts/FormApacRequest', () => ({
    useFormRequest: () => ({ form: { getValues: mockGetValues } }),
}));

jest.mock('@/app/solicitar/apacRequest/services/VerificationService', () => ({
    checkCepValidity: jest.fn(),
    checkAgeProcedureAlert: jest.fn(),
}));

import ApacProgressStepper from '../components/ApacProgressStepper';
import { checkCepValidity, checkAgeProcedureAlert } from '../services/VerificationService';

const FakeForm = React.forwardRef<FormRepository, FormProps & { label: string }>(
    ({ label }, ref) => {
        React.useImperativeHandle(ref, () => ({
            validate: () => ({ success: true, message: 'ok' }),
        }));
        return <div>{label}</div>;
    }
);

function renderStepper() {
    render(
        <GlobalComponentsProvider>
            <ApacProgressStepper>
                <StepForm>
                    <FakeForm label="Passo 0 - Data" />
                </StepForm>
                <StepForm>
                    <FakeForm label="Passo 1 - Paciente" />
                </StepForm>
                <StepForm>
                    <FakeForm label="Passo 2 - Procedimento" />
                </StepForm>
                <StepForm>
                    <FakeForm label="Passo 3 - Fim" />
                </StepForm>
            </ApacProgressStepper>
        </GlobalComponentsProvider>
    );
}

const clickNext = () => fireEvent.click(screen.getByRole('button', { name: /Próximo/i }));

beforeEach(() => {
    jest.clearAllMocks();
    mockGetValues.mockImplementation((path: string) => {
        if (path === 'apacData.patientAddressPostalCode') return '22221036';
        if (path === 'apacData.patientBirthDate') return '12/03/1999';
        if (path === 'apacData.mainProcedureId') return 5;
        return '';
    });
});

test('avança direto quando o CEP é válido', async () => {
    (checkCepValidity as jest.Mock).mockResolvedValue({ available: true, valid: true });
    (checkAgeProcedureAlert as jest.Mock).mockResolvedValue({ available: true, alert: false });

    renderStepper();

    clickNext(); // passo 0 -> 1 (sem checagem)
    await screen.findByText('Passo 1 - Paciente');

    clickNext(); // passo 1 -> 2 (checagem de CEP)
    await waitFor(() => expect(checkCepValidity).toHaveBeenCalledWith('22221036'));
    await screen.findByText('Passo 2 - Procedimento');
});

test('CEP inválido abre modal de confirmação; cancelar mantém no step do paciente', async () => {
    (checkCepValidity as jest.Mock).mockResolvedValue({ available: true, valid: false });

    renderStepper();

    clickNext();
    await screen.findByText('Passo 1 - Paciente');

    clickNext();
    expect(await screen.findByText(/CEP informado não foi encontrado/i)).toBeInTheDocument();

    fireEvent.click(screen.getByText('Corrigir'));

    await waitFor(() =>
        expect(screen.queryByText(/CEP informado não foi encontrado/i)).not.toBeInTheDocument()
    );
    expect(screen.getByText('Passo 1 - Paciente')).toBeInTheDocument();
});

test('CEP inválido: confirmar no modal avança mesmo assim', async () => {
    (checkCepValidity as jest.Mock).mockResolvedValue({ available: true, valid: false });

    renderStepper();

    clickNext();
    await screen.findByText('Passo 1 - Paciente');

    clickNext();
    fireEvent.click(await screen.findByText('Continuar mesmo assim'));

    await screen.findByText('Passo 2 - Procedimento');
});

test('API de CEP indisponível não bloqueia o avanço (sem modal)', async () => {
    (checkCepValidity as jest.Mock).mockResolvedValue({ available: false, valid: true });

    renderStepper();

    clickNext();
    await screen.findByText('Passo 1 - Paciente');

    clickNext();
    await screen.findByText('Passo 2 - Procedimento');
    expect(screen.queryByText(/CEP informado não foi encontrado/i)).not.toBeInTheDocument();
});

test('alerta de idade + procedimento abre modal de confirmação', async () => {
    (checkCepValidity as jest.Mock).mockResolvedValue({ available: true, valid: true });
    (checkAgeProcedureAlert as jest.Mock).mockResolvedValue({
        available: true,
        alert: true,
        message: 'Alerta de idade para este procedimento',
    });

    renderStepper();

    clickNext();
    await screen.findByText('Passo 1 - Paciente');
    clickNext();
    await screen.findByText('Passo 2 - Procedimento');

    clickNext();
    expect(await screen.findByText('Alerta de idade para este procedimento')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Corrigir'));
    await waitFor(() =>
        expect(screen.queryByText('Alerta de idade para este procedimento')).not.toBeInTheDocument()
    );
    expect(screen.getByText('Passo 2 - Procedimento')).toBeInTheDocument();
});

test('API de alerta de idade indisponível não bloqueia o avanço', async () => {
    (checkCepValidity as jest.Mock).mockResolvedValue({ available: true, valid: true });
    (checkAgeProcedureAlert as jest.Mock).mockResolvedValue({ available: false, alert: false });

    renderStepper();

    clickNext();
    await screen.findByText('Passo 1 - Paciente');
    clickNext();
    await screen.findByText('Passo 2 - Procedimento');

    clickNext();
    await screen.findByText('Passo 3 - Fim');
});
