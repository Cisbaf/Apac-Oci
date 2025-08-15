import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/auth";

const API_URL = process.env.DJANGO_API_URL;

function getTargetUrl(request: NextRequest) {
    const url = new URL(request.url);
    const proxyPrefix = "/api/proxy/";
    const endpointPath = url.pathname.startsWith(proxyPrefix)
        ? url.pathname.slice(proxyPrefix.length)
        : url.pathname;
    return `${API_URL}/${endpointPath}${url.search}`;
}

async function proxyHandler(request: NextRequest) {
    const session = await auth();

    if (!session?.accessToken) {
        return NextResponse.json({ error: "Não autenticado" }, { status: 401 });
    }

    const targetUrl = getTargetUrl(request);
    const headers: Record<string, string> = {
        Accept: "application/json",
        Authorization: `Bearer ${session.accessToken}`,
    };

    let body: BodyInit | undefined;
    if (request.method !== "GET" && request.method !== "HEAD") {
        try {
            const json = await request.json();
            body = JSON.stringify(json);
            headers["Content-Type"] = "application/json";
        } catch {
            // Caso o corpo seja vazio ou não seja JSON
        }
    }

    try {
        const res = await fetch(targetUrl, {
            method: request.method,
            headers,
            body,
        });

        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (error: any) {
        console.error(`Proxy ${request.method} error:`, error);
        return NextResponse.json(
            { error: "Erro ao comunicar com a API externa", details: error.message },
            { status: 500 }
        );
    }
}

// Exporta todos os métodos usando o mesmo handler
export const GET = proxyHandler;
export const POST = proxyHandler;
export const PUT = proxyHandler;
export const DELETE = proxyHandler;
export const PATCH = proxyHandler;
