import { NextResponse, type NextRequest } from 'next/server';


const API_BASE_URL = process.env.DJANGO_API_URL || 'http://localhost:8000';

// Rotas públicas que não requerem autenticação
const PUBLIC_ROUTES = [
  '/login',
  '/logout',
  '/api/auth/login',
  '/api/auth/logout',
];

// Verifica se a rota atual é pública
const isPublicRoute = (pathname: string) => {
  return PUBLIC_ROUTES.some(route => {
    if (route.endsWith('.*')) {
      const regex = new RegExp(`^${route.replace(/\.\*$/, '')}.*`);
      return regex.test(pathname);
    }
    return pathname === route;
  });
};
// middleware.ts - Simplificar a verificação
export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (isPublicRoute(pathname)) {
    return NextResponse.next();
  }

  const token = request.cookies.get('token')?.value;
 
  if (!token) {
    return redirectToLogin(request, pathname);
  }

  const response = await fetch(`${API_BASE_URL}/auth/verify/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ token }),
  });

  if (!response.ok) {
    return redirectToLogin(request, pathname);
  }
    return NextResponse.next();
}

// Função auxiliar para redirecionamento
function redirectToLogin(request: NextRequest, fromPath: string) {
  const loginUrl = new URL('/login', request.url);
  loginUrl.searchParams.set('from', fromPath);
  return NextResponse.redirect(loginUrl);
}
// Configuração do middleware
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};

// O CÓDIGO ESTÁ AQUI SÓ PARA SALVAR UM EXEMPLO DE LOGOUT
// export async function logoutUser() {
//   const token = (await cookies()).get('token')?.value;
  
//   if (token) {
//     try {
//       await fetch(`${API_BASE_URL}/auth/logout/`, {
//         method: 'POST',
//         headers: {
//           'Authorization': `Bearer ${token}`,
//         },
//       });
//     } catch (error) {
//       console.error('Logout error:', error);
//     }
//   }
  
//   (await cookies()).delete('token');
// }
