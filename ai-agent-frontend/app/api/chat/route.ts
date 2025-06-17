"use server"

import { NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { prisma } from "@/lib/prisma";

interface Message {
    role: string;
    content: string;
}

export async function POST(req: Request) {
    try {
        const session = await auth();
        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const { message, sessionId } = await req.json();

        if (!message) {
            return new NextResponse("Message is required", { status: 400 });
        }

        // If sessionId is provided, fetch previous messages for context
        let previousMessages: Message[] = [];
        if (sessionId) {
            previousMessages = await prisma.message.findMany({
                where: {
                    sessionId: sessionId,
                },
                orderBy: {
                    createdAt: 'asc',
                },
            });
        }

        // Forward the request to the Python backend with context
        const response = await fetch(`${process.env.WEB_URL}/api/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message,
                session_id: sessionId,
                user_id: session?.userId || null,
                context: previousMessages
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