
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