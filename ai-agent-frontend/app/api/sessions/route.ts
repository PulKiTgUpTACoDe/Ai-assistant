"use server"

import { NextResponse } from 'next/server';
import { auth } from "@clerk/nextjs/server";
import { prisma } from '@/lib/prisma';

export async function GET() {
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

        const sessions = await prisma.session.findMany({
            where: {
                userId: session.userId,
            },
            orderBy: {
                createdAt: 'desc',
            },
            include: {
                messages: {
                    take: 1,
                    orderBy: {
                        createdAt: 'desc',
                    },
                },
            },
        });

        return NextResponse.json(sessions);
    } catch (error) {
        console.error("[SESSIONS_GET_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}

export async function POST(req: Request) {
    try {
        const session = await auth();
        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const { title } = await req.json();

        // Get or create user
        const user = await prisma.user.upsert({
            where: { id: session.userId },
            update: {},
            create: {
                id: session.userId,
                email: "", // Will be updated when user data is available
            },
        });

        const newSession = await prisma.session.create({
            data: {
                userId: session.userId,
                title: title || "New Chat",
            },
        });

        return NextResponse.json(newSession);
    } catch (error) {
        console.error("[SESSIONS_POST_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
} 