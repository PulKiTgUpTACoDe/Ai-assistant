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
        "flex gap-4 p-4",
        isUser ? "flex-row-reverse bg-muted/50" : "bg-background"
      )}
    >
      <div
        className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
          isUser ? "bg-primary mr-10" : "bg-primary/10"
        )}
      >
        {isUser ? (
          <User className="w-4 h-4 text-primary-foreground" />
        ) : (
          <Bot className="w-4 h-4 text-primary" />
        )}
      </div>
      <div className={cn("flex-1 space-y-2", isUser && "text-right")}>
        <div className="text-md font-medium">
          {isUser ? "You" : "AI Assistant"}
        </div>
        <div className="text-md text-muted-foreground whitespace-pre-wrap">
          {message.content}
        </div>
      </div>
    </div>
  );
}
