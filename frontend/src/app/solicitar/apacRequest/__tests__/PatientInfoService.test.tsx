import { formatCns, formatCpf, formatCep } from '../services/PatientInfoService';

describe('formatCns', () => {
    test('limpa CNS com espaços e formata em grupos', () => {
        expect(formatCns('706 0003 4345 8946')).toBe('706 0003 4345 8946');
    });

    test('limpa CNS com traços e pontos', () => {
        expect(formatCns('706.000-3434.5894-6')).toBe('706 0003 4345 8946');
    });

    test('CNS já só com dígitos é formatado corretamente', () => {
        expect(formatCns('706000343458946')).toBe('706 0003 4345 8946');
    });

    test('CNS com quantidade errada de dígitos após limpeza retorna vazio', () => {
        expect(formatCns('706 0003 4345')).toBe('');
    });

    test('valor vazio ou nulo retorna string vazia', () => {
        expect(formatCns('')).toBe('');
        expect(formatCns(null)).toBe('');
        expect(formatCns(undefined)).toBe('');
    });
});

describe('formatCpf', () => {
    test('limpa CPF com pontuação e formata', () => {
        expect(formatCpf('187.149.337-48')).toBe('187.149.337-48');
    });

    test('limpa CPF só com dígitos e espaços', () => {
        expect(formatCpf('187 149 337 48')).toBe('187.149.337-48');
    });
});

describe('formatCep', () => {
    test('limpa CEP com traço e formata', () => {
        expect(formatCep('26265-090')).toBe('26265-090');
    });

    test('limpa CEP com espaços', () => {
        expect(formatCep('26265 090')).toBe('26265-090');
    });
});
