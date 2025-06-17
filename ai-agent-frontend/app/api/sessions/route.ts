"use server"

import { NextResponse } from 'next/server';
import { auth, currentUser } from "@clerk/nextjs/server";
import { prisma } from '@/lib/prisma';

export async function GET() {
    try {
        const session = await auth();
        const user = await currentUser();

        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        // Get or create user with email from Clerk session
        const dbUser = await prisma.user.upsert({
            where: { id: session.userId },
            update: {
                email: user?.emailAddresses[0]?.emailAddress || "",
            },
            create: {
                id: session.userId,
                email: user?.emailAddresses[0]?.emailAddress || "",
                name: user?.fullName || ""
            },
        });

        const sessions = await prisma.session.findMany({
            where: {
                userId: dbUser.id,
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
        const user = await currentUser();

        if (!session?.userId) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const { title, firstMessage } = await req.json();

        // Get or create user with email from Clerk session
        const dbUser = await prisma.user.upsert({
            where: { id: session.userId },
            update: {
                email: user?.emailAddresses[0]?.emailAddress || "",
                name: user?.fullName || ""
            },
            create: {
                id: session.userId,
                email: user?.emailAddresses[0]?.emailAddress || "",
                name: user?.fullName || ""
            },
        });

        // If firstMessage is provided, use it to generate the title
        const sessionTitle = firstMessage
            ? firstMessage.slice(0, 50) + (firstMessage.length > 50 ? "..." : "")
            : title || "New Chat";

        const newSession = await prisma.session.create({
            data: {
                userId: dbUser.id,
                title: sessionTitle,
            },
        });

        return NextResponse.json(newSession);
    } catch (error) {
        console.error("[SESSIONS_POST_ERROR]", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
} 