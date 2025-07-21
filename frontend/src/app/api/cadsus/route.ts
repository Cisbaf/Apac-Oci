import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const API_CADSUS = process.env.API_CADSUS || 'http://192.168.1.10:8014/consult';

export async function POST(request: NextRequest) {
    const json = await request.json();

    const response = await fetch(API_CADSUS, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(json),
    });

     const data = await response.json();
    return NextResponse.json(data, { status: response.status });
}