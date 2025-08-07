
export const PhoneMask = {
    mask: '+0 (___) ___-__-__',
    replacement: { _: /\d/ },
}

export const CpfMask = {
    mask: '___.___.___-__',
    replacement: { _: /\d/ },
}

export const CnsMask = {
  mask: '___ ____ ____ ____',
  replacement: { _: /\d/ },
};

export const BirdDateMsk = {
    mask: '__/__/____',
    replacement: { _: /\d/ },
}

export const CepMask = {
    mask: '_____-___',
    replacement: { _: /\d/ },
}

interface Mask {
  mask: string;
  replacement: { [key: string]: RegExp };
}


export function applyMask(value: string, maskObj: Mask): string {
  const { mask, replacement } = maskObj;
  const result: string[] = [];
  const valueChars = value.replace(/\D/g, '').split(''); // remove tudo que não é número

  let valueIndex = 0;

  for (let i = 0; i < mask.length; i++) {
    const maskChar = mask[i];

    if (replacement[maskChar]) {
      const nextChar = valueChars[valueIndex];

      if (nextChar && replacement[maskChar].test(nextChar)) {
        result.push(nextChar);
        valueIndex++;
      } else {
        result.push('_'); // ou quebre aqui se quiser parar quando faltar caractere
      }
    } else {
      result.push(maskChar);
    }
  }

  return result.join('');
}