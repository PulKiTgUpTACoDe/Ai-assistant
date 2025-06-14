"use client";

import { motion } from "framer-motion";
import { Bot } from "lucide-react";

interface AIAvatarProps {
  isTyping?: boolean;
}

export function AIAvatar({ isTyping = false }: AIAvatarProps) {
  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="relative"
    >
      <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
        <Bot className="w-5 h-5 text-primary" />
      </div>
      {isTyping && (
        <motion.div
          className="absolute -bottom-1 -right-1 w-3 h-3 bg-primary rounded-full"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [1, 0.8, 1],
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      )}
    </motion.div>
  );
}
