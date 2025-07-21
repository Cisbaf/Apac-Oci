import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.DJANGO_API_URL;

function getTargetUrl(request: NextRequest) {
    const url = new URL(request.url);
    const proxyPrefix = "/api/proxy/";
    const endpointPath = url.pathname.startsWith(proxyPrefix)
        ? url.pathname.slice(proxyPrefix.length)
        : url.pathname;
    return `${API_URL}/${endpointPath}${url.search}`;
}

export async function GET(request: NextRequest) {
    const token = request.cookies.get('token')?.value;
    const targetUrl = getTargetUrl(request);
    try {
        const res = await fetch(targetUrl, {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        });

        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (error: any) {
        console.error("Proxy GET error:", error);
        return NextResponse.json(
            { error: "Erro ao comunicar com a API externa", details: error.message },
            { status: 500 }
        );
    }
}

export async function POST(request: NextRequest) {
    return handleProxy(request);
}

export async function PUT(request: NextRequest) {
    return handleProxy(request);
}

export async function DELETE(request: NextRequest) {
    const targetUrl = getTargetUrl(request);
    try {
        const res = await fetch(targetUrl, {
            method: "DELETE",
            headers: {
                "Accept": "application/json",
            },
        });

        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (error: any) {
        console.error("Proxy DELETE error:", error);
        return NextResponse.json(
            { error: "Erro ao comunicar com a API externa", details: error.message },
            { status: 500 }
        );
    }
}

async function handleProxy(request: NextRequest) {
    const token = request.cookies.get('token')?.value;
    const targetUrl = getTargetUrl(request);
    try {
        const headers: Record<string, string> = {
            Accept: "application/json",
            Authorization: `Bearer ${token}`
        };

        let body: BodyInit | undefined;
        
        const json = await request.json();
        body = JSON.stringify(json);
        headers["Content-Type"] = "application/json";

        const res = await fetch(targetUrl, {
            method: request.method,
            headers,
            body,
        });

        const data = await res.json();
        return NextResponse.json(data, { status: res.status });

    } catch (error: any) {
        console.error("Proxy error:", error);
        return NextResponse.json(
            { error: "Erro ao comunicar com a API externa", details: error.message },
            { status: 500 }
        );
    }
}
