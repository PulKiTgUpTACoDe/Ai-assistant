"use server";

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { auth } from '@clerk/nextjs/server';

interface RouteParams {
    params: {
        id: string;
    };
}

export async function GET(request: Request, { params }: RouteParams) {
    try {
        const session = await auth();
        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const chatSession = await prisma.session.findUnique({
            where: {
                id: params.id,
            },
        });

        if (!chatSession) {
            return new NextResponse("Session not found", { status: 404 });
        }

        if (chatSession.userId !== session.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const messages = await prisma.message.findMany({
            where: {
                sessionId: params.id,
            },
            orderBy: {
                createdAt: 'asc',
            },
        });

        return NextResponse.json(messages);
    } catch (error) {
        console.error("[MESSAGES_GET_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}

export async function POST(request: Request, { params }: RouteParams) {
    try {
        const session = await auth();
        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const { role, content } = await request.json();

        // Verify session ownership
        const chatSession = await prisma.session.findUnique({
            where: {
                id: params.id,
            },
        });

        if (!chatSession) {
            return new NextResponse("Session not found", { status: 404 });
        }

        if (chatSession.userId !== session.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        // Create message
        const message = await prisma.message.create({
            data: {
                sessionId: params.id,
                role,
                content,
            },
        });

        return NextResponse.json(message);
    } catch (error) {
        console.error("[MESSAGE_POST_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
} 