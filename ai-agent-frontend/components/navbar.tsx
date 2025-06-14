"use client";

import { SignedIn, SignedOut, UserButton } from "@clerk/nextjs";

import { ThemeToggle } from "./theme-toggle";
import { Button } from "./ui/button";
import { Logo } from "./logo";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { NavbarProps } from "@/lib/types";
import { cn } from "@/lib/utils";

export function Navbar({ className }: NavbarProps) {
  return (
    <nav
      className={cn(
        "sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60",
        className
      )}
    >
      <div className="container flex h-16 items-center justify-between pl-10">
        <div className="flex items-center">
          <div className="flex items-center gap-5 md:gap-6">
            <Logo size="sm" className="md:scale-100 scale-90" />
            <HoverCard>
              <HoverCardTrigger asChild>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Link
                    href="/pricing"
                    className="relative inline-flex items-center justify-center px-3 py-1.5 md:px-4 md:py-2 text-sm md:text-md font-medium transition-colors hover:text-primary group hover:bg-accent/100 bg-accent/60 dark:hover:bg-accent/70 rounded-md dark:bg-accent/20"
                  >
                    <span className="relative z-10 text-neutral-600 dark:hover:text-neutral-300 hover:text-black">
                      Pricing
                    </span>
                    <motion.div
                      className="absolute inset-0 bg-primary/5 dark:bg-primary/10 rounded-md"
                      initial={{ scale: 0 }}
                      whileHover={{ scale: 1 }}
                      transition={{ duration: 0.2 }}
                    />
                  </Link>
                </motion.div>
              </HoverCardTrigger>
              <HoverCardContent className="w-80">
                <div className="space-y-2">
                  <h4 className="font-semibold">Check out our plans</h4>
                  <p className="text-sm text-muted-foreground">
                    Choose the perfect plan for your needs. Start free or
                    upgrade to unlock more features.
                  </p>
                </div>
              </HoverCardContent>
            </HoverCard>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <ThemeToggle />

          <SignedOut>
            <div className="flex items-center gap-2">
              <Link href="/sign-in">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link href="/sign-up">
                <Button size="sm">Sign Up</Button>
              </Link>
            </div>
          </SignedOut>

          <SignedIn>
            <div className="flex items-center gap-2">
              <UserButton
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    avatarBox:
                      "w-10 h-10 hover:ring-2 hover:ring-accent/50 transition-all duration-300",
                    userButtonPopoverCard: "w-64",
                  },
                }}
              />
            </div>
          </SignedIn>
        </div>
      </div>
    </nav>
  );
}
