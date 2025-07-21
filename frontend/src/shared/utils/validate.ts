import { generatePattern } from '@react-input/mask';

export function validateMask(mask: any, value: string) {
    const pattern = generatePattern('full', mask);
    const regex = new RegExp(pattern);
    return regex.test(value)
}

export function isValidCPF(cpf: string): boolean {
  cpf = cpf.replace(/[^\d]+/g, '');
  if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

  let sum = 0, rest;
  for (let i = 1; i <= 9; i++) sum += parseInt(cpf[i - 1]) * (11 - i);
  rest = (sum * 10) % 11;
  if (rest === 10 || rest === 11) rest = 0;
  if (rest !== parseInt(cpf[9])) return false;

  sum = 0;
  for (let i = 1; i <= 10; i++) sum += parseInt(cpf[i - 1]) * (12 - i);
  rest = (sum * 10) % 11;
  if (rest === 10 || rest === 11) rest = 0;

  return rest === parseInt(cpf[10]);
}

export function isValidCNS(cns: string): boolean {
  // Remove qualquer caractere que não seja número
  cns = cns.replace(/\D/g, '');

  if (cns.length !== 15) return false;

  const firstChar = cns.charAt(0);

  if ('12789'.includes(firstChar)) {
    // Validação baseada na soma ponderada
    let soma = 0;
    for (let i = 0; i < 15; i++) {
      soma += parseInt(cns.charAt(i), 10) * (15 - i);
    }
    return soma % 11 === 0;
  }

  return false;
}
