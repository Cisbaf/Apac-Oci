import { DefaultSession, DefaultUser } from "next-auth";

declare module "next-auth" {
  interface Session {
    accessToken?: string;
    user?: {
      id?: string | number;
      name?: string | null;
      email?: string | null;
      // adicione outros campos que você espera no user
    } & DefaultSession["user"];
  }

  interface User extends DefaultUser {
    accessToken?: string;
    refreshToken?: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    accessTokenExpires?: number;
    error?: string;
    user?: {
      id?: string | number;
      name?: string | null;
      email?: string | null;
    };
  }
}
