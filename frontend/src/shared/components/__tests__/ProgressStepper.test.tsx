import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ProgressStepper } from '@/shared/components/ProgressStepper';
import StepForm from '@/shared/components/StepComponent';
import { GlobalComponentsProvider } from '@/shared/context/GlobalUIContext';
import { FormRepository, FormProps } from '@/shared/repositories/formRepository';

const FakeForm = React.forwardRef<FormRepository, FormProps & { label: string }>(
    ({ label }, ref) => {
        React.useImperativeHandle(ref, () => ({
            validate: () => ({ success: true, message: 'ok' }),
        }));
        return <div>{label}</div>;
    }
);

function renderStepper(onBeforeNext?: (stepIndex: number) => Promise<boolean>) {
    render(
        <GlobalComponentsProvider>
            <ProgressStepper onBeforeNext={onBeforeNext}>
                <StepForm>
                    <FakeForm label="Passo 1" />
                </StepForm>
                <StepForm>
                    <FakeForm label="Passo 2" />
                </StepForm>
            </ProgressStepper>
        </GlobalComponentsProvider>
    );
}

test('avança normalmente quando não há onBeforeNext', async () => {
    renderStepper();

    expect(screen.getByText('Passo 1')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Próximo/i }));

    await waitFor(() => expect(screen.getByText('Passo 2')).toBeInTheDocument());
});

test('avança quando onBeforeNext resolve true', async () => {
    const onBeforeNext = jest.fn().mockResolvedValue(true);
    renderStepper(onBeforeNext);

    fireEvent.click(screen.getByRole('button', { name: /Próximo/i }));

    await waitFor(() => expect(onBeforeNext).toHaveBeenCalledWith(0));
    await waitFor(() => expect(screen.getByText('Passo 2')).toBeInTheDocument());
});

test('bloqueia avanço quando onBeforeNext resolve false', async () => {
    const onBeforeNext = jest.fn().mockResolvedValue(false);
    renderStepper(onBeforeNext);

    fireEvent.click(screen.getByRole('button', { name: /Próximo/i }));

    await waitFor(() => expect(onBeforeNext).toHaveBeenCalledWith(0));
    expect(screen.getByText('Passo 1')).toBeInTheDocument();
    expect(screen.queryByText('Passo 2')).not.toBeInTheDocument();
});
