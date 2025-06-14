"use server"

import { NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';

export async function POST(req: Request) {
    try {
        const { message, sessionId } = await req.json();
        const session = await auth();

        // Forward the request to the Python backend
        const response = await fetch("http://localhost:8000/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message,
                session_id: sessionId,
                user_id: session?.userId || null
            }),
        });

        if (!response.ok) {
            throw new Error("Failed to get response from backend");
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error("[CHAT_ERROR]", error);
        return new NextResponse(
            error instanceof Error ? error.message : "Internal Error",
            { status: 500 }
        );
    }
} 