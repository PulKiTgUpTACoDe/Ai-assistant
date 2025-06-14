"use client";

import { motion } from "framer-motion";
import { Sparkles, Bot, Brain } from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface LogoProps {
  className?: string;
  size?: "sm" | "md" | "lg";
  animated?: boolean;
}

export function Logo({ className, size = "md", animated = true }: LogoProps) {
  const sizeClasses = {
    sm: "w-8 h-8",
    md: "w-12 h-12",
    lg: "w-16 h-16",
  };

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <Link href="/">
        <motion.div
          initial={animated ? { scale: 0.8, opacity: 0 } : false}
          animate={animated ? { scale: 1, opacity: 1 } : false}
          className={cn(
            "relative rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 p-2 backdrop-blur-sm",
            sizeClasses[size]
          )}
        >
          <motion.div
            initial={animated ? { rotate: -10 } : false}
            animate={animated ? { rotate: 10 } : false}
            transition={{
              duration: 2,
              repeat: Infinity,
              repeatType: "reverse",
              ease: "easeInOut",
            }}
            className="relative h-full w-full"
          >
            <Bot className="h-full w-full text-primary" />
          </motion.div>
          <motion.div
            initial={animated ? { scale: 0 } : false}
            animate={animated ? { scale: 1 } : false}
            transition={{ delay: 0.4 }}
            className="absolute -bottom-1 -right-1"
          >
            <Brain className="h-4 w-4 text-primary/80" />
          </motion.div>
        </motion.div>
      </Link>
      <div className="flex flex-col">
        <motion.span
          initial={animated ? { x: -20, opacity: 0 } : false}
          animate={animated ? { x: 0, opacity: 1 } : false}
          transition={{ delay: 0.2 }}
          className="text-xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent"
        >
          AI Agent
        </motion.span>
        <motion.span
          initial={animated ? { x: -20, opacity: 0 } : false}
          animate={animated ? { x: 0, opacity: 1 } : false}
          transition={{ delay: 0.3 }}
          className="text-xs text-muted-foreground"
        >
          Your Intelligent Assistant
        </motion.span>
      </div>
    </div>
  );
}
