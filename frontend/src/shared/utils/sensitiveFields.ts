export function removeSensitiveFields(user: any) {
    const { password, ...safeUser } = user;
    return safeUser;
  }
  