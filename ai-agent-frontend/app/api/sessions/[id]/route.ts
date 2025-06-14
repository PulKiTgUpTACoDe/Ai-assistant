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

        // Get or create user
        const user = await prisma.user.upsert({
            where: { id: session.userId },
            update: {},
            create: {
                id: session.userId,
                email: "", // Will be updated when user data is available
            },
        });

        const chatSession = await prisma.session.findUnique({
            where: {
                id: params.id,
            },
            include: {
                messages: {
                    orderBy: {
                        createdAt: 'asc',
                    },
                },
            },
        });

        if (!chatSession) {
            return new NextResponse("Session not found", { status: 404 });
        }

        if (chatSession.userId !== session.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        return NextResponse.json(chatSession);
    } catch (error) {
        console.error("[SESSION_GET_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}

export async function PATCH(request: Request, { params }: RouteParams) {
    try {
        const session = await auth();
        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const { title } = await request.json();

        // Get or create user
        const user = await prisma.user.upsert({
            where: { id: session.userId },
            update: {},
            create: {
                id: session.userId,
                email: "", // Will be updated when user data is available
            },
        });

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

        const updatedSession = await prisma.session.update({
            where: {
                id: params.id,
            },
            data: {
                title,
            },
        });

        return NextResponse.json(updatedSession);
    } catch (error) {
        console.error("[SESSION_PATCH_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}

export async function DELETE(request: Request, { params }: RouteParams) {
    try {
        const session = await auth();
        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        // Get or create user
        const user = await prisma.user.upsert({
            where: { id: session.userId },
            update: {},
            create: {
                id: session.userId,
                email: "", // Will be updated when user data is available
            },
        });

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

        await prisma.session.delete({
            where: {
                id: params.id,
            },
        });

        return new NextResponse(null, { status: 204 });
    } catch (error) {
        console.error("[SESSION_DELETE_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
} 