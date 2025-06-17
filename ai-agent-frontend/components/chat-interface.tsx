"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, Bot } from "lucide-react";
import { ChatMessage } from "@/components/chat-message";
import { useAuth } from "@clerk/nextjs";
import { useQuery } from "@/lib/context/query-context";
import { useSession } from "@/lib/context/session-context";
import { toast } from "sonner";
import { Message } from "@/lib/context/session-context";
import { cn } from "@/lib/utils";

const LOCAL_STORAGE_KEY = "ai_agent_messages";

function LoadingMessage() {
  return (
    <div className="flex gap-2 md:gap-4 p-2 md:p-4 animate-pulse">
      <div className="w-6 h-6 md:w-8 md:h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
        <Bot className="w-3 h-3 md:w-4 md:h-4 text-primary" />
      </div>
      <div className="flex-1 space-y-1.5 md:space-y-2">
        <div className="h-3 md:h-4 w-16 md:w-24 bg-muted rounded" />
        <div className="h-3 md:h-4 w-32 md:w-48 bg-muted rounded" />
        <div className="h-3 md:h-4 w-24 md:w-32 bg-muted rounded" />
      </div>
    </div>
  );
}

function AnimatedMessage({
  content,
  onComplete,
}: {
  content: string;
  onComplete: () => void;
}) {
  const [displayedContent, setDisplayedContent] = useState("");
  const indexRef = useRef(0);
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    indexRef.current = 0;
    setDisplayedContent("");

    const animate = () => {
      if (indexRef.current < content.length) {
        setDisplayedContent((prev) => prev + content[indexRef.current]);
        indexRef.current++;
        animationFrameRef.current = requestAnimationFrame(animate);
      } else {
        cancelAnimationFrame(animationFrameRef.current!);
        onComplete(); // Notify when animation is done
      }
    };

    animationFrameRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [content, onComplete]);

  return (
    <div className="flex gap-2 md:gap-4 p-2 md:p-4">
      <div className="w-6 h-6 md:w-8 md:h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
        <Bot className="w-3 h-3 md:w-4 md:h-4 text-primary" />
      </div>
      <div className="flex-1">
        <p className="text-xs md:text-sm text-muted-foreground mb-1">
          AI Assistant
        </p>
        <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap break-words">
          {displayedContent}
          <motion.span
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 1, repeat: Infinity }}
            className="inline-block w-0.5 md:w-1 h-3 md:h-4 bg-primary ml-0.5 md:ml-1 align-middle"
          />
        </p>
      </div>
    </div>
  );
}

export function ChatInterface() {
  const { currentSession, addMessage } = useSession();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { isSignedIn } = useAuth();
  const { incrementQueryCount, remainingQueries, isLimitReached } = useQuery();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [localMessages, setLocalMessages] = useState<Message[]>([]);
  const [currentResponse, setCurrentResponse] = useState<string>("");

  useEffect(() => {
    if (!isSignedIn) {
      const savedMessages = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (savedMessages) {
        setLocalMessages(JSON.parse(savedMessages));
      }
    }
  }, [isSignedIn]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isSignedIn && currentSession?.messages) {
      scrollToBottom();
    } else if (!isSignedIn) {
      scrollToBottom();
    }
  }, [isSignedIn, currentSession?.messages, localMessages, currentResponse]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);
    setCurrentResponse("");

    try {
      // Add user message
      if (isSignedIn) {
        if (!currentSession) return;
        await addMessage("user", userMessage);
      } else {
        const newUserMsg: Message = {
          id: Date.now().toString(),
          role: "user",
          content: userMessage,
          createdAt: new Date().toISOString(),
        };
        setLocalMessages((prev) => {
          const updated = [...prev, newUserMsg];
          localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(updated));
          return updated;
        });
      }

      // Get AI response
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          ...(isSignedIn && currentSession
            ? { sessionId: currentSession.id }
            : {}),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || "Failed to get response");
      }

      const data = await response.json();
      setCurrentResponse(data.response); // Animate this
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : "Failed to send message"
      );
      console.error("Chat error:", error);
      setIsLoading(false);
    }
  };

  if (isSignedIn && !currentSession) {
    return (
      <div className="flex items-center justify-center h-full w-full">
        <p className="text-muted-foreground">
          Select or create a session to start chatting
        </p>
      </div>
    );
  }

  const messages = isSignedIn ? currentSession?.messages : localMessages;

  return (
    <div
      className={cn(
        "flex flex-col h-full w-full bg-background relative",
        isSignedIn ? "" : "left-0 md:left-60"
      )}
    >
      <div className="flex-1 overflow-y-auto px-1 sm:px-2 md:p-4 space-y-2 md:space-y-4 w-full md:w-5xl md:min-w-2xl pb-24 md:pb-30">
        {!messages || messages.length === 0 ? (
          <motion.div
            className={cn(
              "flex flex-col items-center justify-center h-[60vh] text-center space-y-3 md:space-y-4 w-full px-2 sm:px-4 md:pl-28",
              isSignedIn ? "bg-background/50" : "bg-muted/20"
            )}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div
              animate={{
                scale: [1, 1.1, 1],
                rotate: [0, 5, -5, 0],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                repeatType: "reverse",
              }}
              className={cn(
                "p-3 md:p-4 rounded-full",
                isSignedIn ? "bg-primary/10" : "bg-muted/30"
              )}
            >
              <Bot
                className={cn(
                  "w-7 h-7 md:w-12 md:h-12",
                  isSignedIn ? "text-primary" : "text-muted-foreground"
                )}
              />
            </motion.div>
            <motion.p
              className={cn(
                "text-sm sm:text-base md:text-lg max-w-[280px] sm:max-w-md md:max-w-2xl px-2",
                isSignedIn ? "text-foreground" : "text-muted-foreground"
              )}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.5 }}
            >
              {isSignedIn
                ? "Your intelligent assistant is ready to help you with any task. Just type your message below to get started."
                : "Try our AI assistant. Sign in for unlimited access."}
            </motion.p>
          </motion.div>
        ) : (
          <div className="w-full md:min-w-4xl mx-auto">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}

            {isLoading && currentResponse && (
              <AnimatedMessage
                content={currentResponse}
                onComplete={async () => {
                  if (isSignedIn) {
                    await addMessage("assistant", currentResponse);
                  } else {
                    const newMessage: Message = {
                      id: Date.now().toString(),
                      role: "assistant",
                      content: currentResponse,
                      createdAt: new Date().toISOString(),
                    };
                    setLocalMessages((prev) => {
                      const updated = [...prev, newMessage];
                      localStorage.setItem(
                        LOCAL_STORAGE_KEY,
                        JSON.stringify(updated)
                      );
                      return updated;
                    });
                    incrementQueryCount();
                  }

                  setCurrentResponse("");
                  setIsLoading(false);
                }}
              />
            )}

            {isLoading && !currentResponse && <LoadingMessage />}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="fixed bottom-0 left-0 md:left-10 border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 w-full">
        <form
          onSubmit={handleSubmit}
          className="w-full max-w-4xl mx-auto p-2 md:p-4"
        >
          <div className="flex gap-1.5 md:gap-2">
            <Textarea
              placeholder={
                isSignedIn
                  ? "Type your message..."
                  : `Try our AI assistant (${remainingQueries} queries remaining)...`
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="min-h-[52px] md:min-h-[60px] resize-none flex-1 text-sm md:text-base px-3 py-2 md:px-4 md:py-3"
              disabled={isLoading || (!isSignedIn && isLimitReached)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <Button
              type="submit"
              size="icon"
              disabled={
                isLoading || !input.trim() || (!isSignedIn && isLimitReached)
              }
              className="shrink-0 h-[52px] w-[52px] md:h-10 md:w-10"
            >
              {isLoading ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{
                    duration: 1,
                    repeat: Infinity,
                    ease: "linear",
                  }}
                >
                  <Send className="h-4 w-4" />
                </motion.div>
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
