"use client";

import { useQuery } from "@/lib/context/query-context";
import { useAuth } from "@clerk/nextjs";
import { ChatInterface } from "@/components/chat-interface";
import { AuthPrompt } from "@/components/auth-prompt";
import { SessionSidebar } from "@/components/session-sidebar";
import { useEffect } from "react";
import { useSession } from "@/lib/context/session-context";
import {
  Sidebar,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";

export default function Home() {
  const { isLimitReached } = useQuery();
  const { isSignedIn } = useAuth();
  const { sessions, currentSession, createSession } = useSession();

  useEffect(() => {
    if (isSignedIn && sessions.length === 0) {
      createSession("New Chat");
    }
  }, [isSignedIn, sessions.length, createSession]);

  if (!isSignedIn && isLimitReached) {
    return <AuthPrompt />;
  }

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="min-h-screen flex flex-col">
        <div className="flex flex-1 h-[calc(100vh-4rem)]">
          {isSignedIn && (
            <>
              <Sidebar>
                <SessionSidebar />
              </Sidebar>
              <div className="fixed top-20 left-4 z-10 md:hidden">
                <SidebarTrigger />
              </div>
            </>
          )}
          <div className="flex-1">
            <ChatInterface />
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
}
