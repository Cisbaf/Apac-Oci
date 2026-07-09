import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ConfirmDialog, { ConfirmDialogHandles } from '@/shared/components/ConfirmDialog';

function Harness() {
    const ref = React.useRef<ConfirmDialogHandles>(null);
    const [result, setResult] = React.useState<string>('');

    return (
        <>
            <button
                onClick={async () => {
                    const confirmed = await ref.current!.confirm('Mensagem de aviso de teste');
                    setResult(confirmed ? 'confirmado' : 'cancelado');
                }}
            >
                Abrir
            </button>
            <div data-testid="result">{result}</div>
            <ConfirmDialog ref={ref} />
        </>
    );
}

test('resolve true quando o usuário confirma o aviso', async () => {
    render(<Harness />);

    fireEvent.click(screen.getByText('Abrir'));
    expect(await screen.findByText('Mensagem de aviso de teste')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Continuar mesmo assim'));

    await waitFor(() => expect(screen.getByTestId('result')).toHaveTextContent('confirmado'));
});

test('resolve false quando o usuário cancela o aviso', async () => {
    render(<Harness />);

    fireEvent.click(screen.getByText('Abrir'));
    expect(await screen.findByText('Mensagem de aviso de teste')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Corrigir'));

    await waitFor(() => expect(screen.getByTestId('result')).toHaveTextContent('cancelado'));
});
