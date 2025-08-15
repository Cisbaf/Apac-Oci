import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import { jwtDecode } from "jwt-decode";

const BACKEND = process.env.DJANGO_API_URL;

async function refreshAccessToken(token: any) {
  try {
    const res = await fetch(BACKEND + "/auth/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: token.refreshToken }),
    });

    if (!res.ok) {
      throw new Error("Erro ao renovar token");
    }

    const refreshed = await res.json();
    const decoded: any = jwtDecode(refreshed.access);
    return {
      ...token,
      accessToken: refreshed.access,
      accessTokenExpires: decoded.exp * 1000,
      // refreshToken: refreshed.refresh ?? token.refreshToken, // se o backend retornar um novo refresh
    };
  } catch (error) {
    console.error("Erro no refreshAccessToken:", error);
    return {
      ...token,
      error: "RefreshAccessTokenError",
    };
  }
}


export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      // You can specify which fields should be submitted, by adding keys to the `credentials` object.
      // e.g. domain, username, password, 2FA token, etc.
        credentials: {
        username: { label: "Usuário", type: "text" },
        password: { label: "Senha", type: "password" },
      },
      authorize: async (credentials) => {
        const res = await fetch(BACKEND + "/auth/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: credentials?.username,
            password: credentials?.password,
          }),
        });

        if (!res.ok) return null;

        const user = await res.json();

        if (user && user.access && user.user) {
          return {
            accessToken: user.access,
            refreshToken: user.refresh,
            ...user.user, // espalha as propriedades do usuário
          };
        }
        
        return null;
      },
    }),
  ],
  callbacks: {
async jwt({ token, user }) {
  // Quando o usuário loga pela primeira vez
  if (user) {
    const decoded: any = jwtDecode(String(user.accessToken));
    token.accessToken = user.accessToken;
    token.refreshToken = user.refreshToken;
    token.user = user;
    token.accessTokenExpires = decoded.exp * 1000; // exp vem em segundos, guardamos em ms
    return token;
  }

  // Se o access token ainda não expirou, retorna como está
  if (Date.now() < (token.accessTokenExpires as number)) {
    return token;
  }

  // Caso contrário, tenta renovar
  return await refreshAccessToken(token);
},

async session({ session, token }) {
  session.accessToken = token.accessToken as string;
  session.user = token.user as any;
  return session;
},
  },

  session: {
    strategy: "jwt",
  },
    secret: process.env.NEXTAUTH_SECRET
})