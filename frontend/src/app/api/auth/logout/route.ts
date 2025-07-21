import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST() {
  // Criar a resposta
  const response = NextResponse.json(
    { message: 'Logout realizado com sucesso' },
    { status: 200 }
  );

  // Remover o cookie
  response.cookies.delete('token');

  // Alternativamente, você pode definir o cookie com data de expiração no passado
  // response.cookies.set('token', '', {
  //   httpOnly: true,
  //   secure: process.env.NODE_ENV === 'production',
  //   expires: new Date(0),
  //   path: '/',
  // });

  return response;
}

// Garantir que apenas POST seja permitido para logout
export async function GET() {
  return NextResponse.json(
    { message: 'Method not allowed' },
    { status: 405 }
  );
}