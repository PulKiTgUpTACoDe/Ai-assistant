"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { Message } from "@/lib/context/session-context";
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex gap-2 md:gap-4 p-2 md:p-4",
        isUser ? "flex-row-reverse bg-muted/50" : "bg-background"
      )}
    >
      <div
        className={cn(
          "w-6 h-6 md:w-8 md:h-8 rounded-full flex items-center justify-center shrink-0",
          isUser ? "bg-primary md:mr-10 mr-2" : "bg-primary/10"
        )}
      >
        {isUser ? (
          <User className="w-3 h-3 md:w-4 md:h-4 text-primary-foreground" />
        ) : (
          <Bot className="w-3 h-3 md:w-4 md:h-4 text-primary" />
        )}
      </div>
      <div
        className={cn("flex-1 space-y-1 md:space-y-2", isUser && "text-right")}
      >
        <div className="text-sm md:text-md font-medium">
          {isUser ? "You" : "AI Assistant"}
        </div>
        <div className="text-sm md:text-md text-muted-foreground whitespace-pre-wrap break-words">
          {message.content}
        </div>
      </div>
    </div>
  );
}
