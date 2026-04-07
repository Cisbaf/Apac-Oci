export function identifyGroup(codMainProcedure: string) {
  if (!codMainProcedure) {
    return false;
  }

  // Regra: subgrupo 0901
  const isSubgrupo0901 = codMainProcedure.startsWith("0901");
  if (!isSubgrupo0901) {
    return false;
  }

  return true;
}

export function isBiopsiaAllowed(
  codMainProcedure: string,
  nameProcedureSecondary: string
): boolean {
  if (!codMainProcedure || !nameProcedureSecondary) {
    return false;
  }

  // Regra: subgrupo 0901
  const isSubgrupo0901 = codMainProcedure.startsWith("0901");
  if (!isSubgrupo0901) {
    return false;
  }

  // Normaliza string (remove acento + lowercase)
  const normalize = (text: string) =>
    text
      .normalize("NFD") // separa acentos
      .replace(/[\u0300-\u036f]/g, "") // remove acentos
      .toLowerCase();

  const normalizedName = normalize(nameProcedureSecondary);
  // Verifica "biopsia"
  return normalizedName.includes("biopsia");
}