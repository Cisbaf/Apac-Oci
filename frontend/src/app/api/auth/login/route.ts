import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const API_BASE_URL = process.env.DJANGO_API_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  const { username, password } = await request.json();

  if (!username || !password) {
    return new NextResponse("É requerido usuário e senha!", { status: 400 });
  }

  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    return new NextResponse(await response.text(), { status: 400 });
  }

  const data = await response.json();
  const token = data.access || data.token;

  // Criar a resposta com o corpo
  const res = NextResponse.json(data, { status: 200 });

  // Definir o cookie HTTP-only
  res.cookies.set('token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 30 * 24 * 60 * 60, // 1 mês em segundos
    path: '/',
  });

  
  return res;
}

// Garantir que apenas POST seja permitido
export async function GET() {
  return NextResponse.json(
    { message: 'Method not allowed' },
    { status: 405 }
  );
}
