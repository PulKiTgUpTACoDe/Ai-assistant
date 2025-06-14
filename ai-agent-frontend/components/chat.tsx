"use client";

import { useQuery } from "@/lib/context/query-context";
import { useAuth } from "@clerk/nextjs";
import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { ChatMessage } from "./chat-message";
import { Send } from "lucide-react";

export function Chat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<
    Array<{ role: "user" | "assistant"; content: string }>
  >([]);
  const { incrementQueryCount, isLimitReached, remainingQueries } = useQuery();
  const { isSignedIn } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Check if user has reached the limit
    if (!isSignedIn && isLimitReached) {
      return;
    }

    // Add user message
    const userMessage = { role: "user" as const, content: message };
    setMessages((prev) => [...prev, userMessage]);
    setMessage("");

    // Increment query count for non-signed-in users
    if (!isSignedIn) {
      incrementQueryCount();
    }

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const data = await response.json();

      // Add assistant message
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
        },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            content={msg.content}
            isUser={msg.role === "user"}
          />
        ))}
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={
              isLimitReached && !isSignedIn
                ? "Please sign in to continue chatting"
                : !isSignedIn
                ? `Type your message... (${remainingQueries} queries remaining)`
                : "Type your message..."
            }
            disabled={isLimitReached && !isSignedIn}
            className="flex-1"
          />
          <Button
            type="submit"
            disabled={!message.trim() || (isLimitReached && !isSignedIn)}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </div>
  );
}
