export function removeSensitiveFields(user: Record<string, unknown>) {
    // password é extraído de propósito, só para excluí-lo de safeUser.
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { password, ...safeUser } = user;
    return safeUser;
  }
