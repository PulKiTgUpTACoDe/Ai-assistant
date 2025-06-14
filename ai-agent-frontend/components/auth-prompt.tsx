"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import Link from "next/link";
import { motion } from "framer-motion";
import { Logo } from "@/components/logo";

export function AuthPrompt() {
  return (
    <main className="flex-1 flex items-center justify-center p-4 mt-[7%]">
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Card className="w-full max-w-md p-8 space-y-6">
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-center space-y-2"
          >
            <Logo size="lg" />
            <p className="text-muted-foreground">
              You've reached the limit. Sign in to continue
              using the AI assistant.
            </p>
          </motion.div>
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col gap-4"
          >
            <Link href="/sign-in">
                <Button variant="ghost" size="lg" className="w-full">
                  Sign In
                </Button>
              </Link>
              <Link href="/sign-up">
                <Button size="lg" className="w-full">Create Account</Button>
              </Link>
          </motion.div>
        </Card>
      </motion.div>
    </main>
  );
}
