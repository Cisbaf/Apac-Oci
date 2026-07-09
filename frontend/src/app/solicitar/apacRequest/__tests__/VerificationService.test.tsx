import { checkCepValidity, checkAgeProcedureAlert } from '../services/VerificationService';

describe('checkCepValidity', () => {
    afterEach(() => {
        jest.restoreAllMocks();
    });

    test('CEP com menos de 8 dígitos é tratado como inválido, mas disponível', async () => {
        const result = await checkCepValidity('123');
        expect(result).toEqual({ available: true, valid: false });
    });

    test('CEP existente retorna valid true', async () => {
        global.fetch = jest.fn().mockResolvedValue({
            ok: true,
            json: async () => ({ logradouro: 'Rua X' }),
        }) as any;

        const result = await checkCepValidity('22221036');
        expect(result).toEqual({ available: true, valid: true });
    });

    test('CEP inexistente (ViaCEP retorna erro) marca valid false', async () => {
        global.fetch = jest.fn().mockResolvedValue({
            ok: true,
            json: async () => ({ erro: true }),
        }) as any;

        const result = await checkCepValidity('00000000');
        expect(result).toEqual({ available: true, valid: false });
    });

    test('falha de rede marca indisponível e não bloqueia o formulário', async () => {
        global.fetch = jest.fn().mockRejectedValue(new Error('network error')) as any;

        const result = await checkCepValidity('22221036');
        expect(result.available).toBe(false);
        expect(result.valid).toBe(true);
    });

    test('resposta HTTP não ok marca indisponível', async () => {
        global.fetch = jest.fn().mockResolvedValue({ ok: false }) as any;

        const result = await checkCepValidity('22221036');
        expect(result.available).toBe(false);
    });
});

describe('checkAgeProcedureAlert', () => {
    afterEach(() => {
        jest.restoreAllMocks();
    });

    test('sem procedimento selecionado não dispara verificação nem alerta', async () => {
        const result = await checkAgeProcedureAlert('12/03/1999', 0);
        expect(result).toEqual({ available: true, alert: false });
    });

    test('data de nascimento incompleta não dispara verificação nem alerta', async () => {
        const result = await checkAgeProcedureAlert('12/03', 5);
        expect(result).toEqual({ available: true, alert: false });
    });

    test('API retorna alerta para a combinação idade + procedimento', async () => {
        global.fetch = jest.fn().mockResolvedValue({
            ok: true,
            json: async () => ({ alert: true, message: 'Procedimento restrito por idade' }),
        }) as any;

        const result = await checkAgeProcedureAlert('12/03/2015', 5);

        expect(result).toEqual({ available: true, alert: true, message: 'Procedimento restrito por idade' });
        expect(global.fetch).toHaveBeenCalledWith(
            '/api/proxy/procedure/apac/check-age-alert/',
            expect.objectContaining({
                method: 'POST',
                body: JSON.stringify({ procedure_id: 5, birth_date: '2015-03-12' }),
            })
        );
    });

    test('API retorna sem alerta quando a idade é compatível', async () => {
        global.fetch = jest.fn().mockResolvedValue({
            ok: true,
            json: async () => ({ alert: false }),
        }) as any;

        const result = await checkAgeProcedureAlert('12/03/1999', 5);
        expect(result.alert).toBe(false);
        expect(result.available).toBe(true);
    });

    test('indisponibilidade da API (erro de rede) não bloqueia o formulário', async () => {
        global.fetch = jest.fn().mockRejectedValue(new Error('timeout')) as any;

        const result = await checkAgeProcedureAlert('12/03/1999', 5);
        expect(result).toEqual({ available: false, alert: false });
    });

    test('resposta HTTP não ok marca indisponível', async () => {
        global.fetch = jest.fn().mockResolvedValue({ ok: false }) as any;

        const result = await checkAgeProcedureAlert('12/03/1999', 5);
        expect(result.available).toBe(false);
    });
});
