import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ClerkProvider } from "@clerk/nextjs";
import { QueryProvider } from "@/lib/context/query-context";
import { ThemeProvider } from "@/components/theme-provider";
import { QueryLimitWarning } from "@/components/query-limit-warning";
import { Navbar } from "@/components/navbar";
import { Toaster } from "@/components/ui/sonner";
import { SessionProvider } from "@/lib/context/session-context";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Agent",
  description: "Your AI-powered assistant",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <QueryProvider>
        <SessionProvider>
          <html lang="en" suppressHydrationWarning>
            <body className={inter.className}>
              <ThemeProvider
                attribute="class"
                defaultTheme="system"
                enableSystem
                disableTransitionOnChange
              >
                <div className="min-h-screen flex flex-col">
                  <Navbar />
                  <main className="flex-1">{children}</main>
                </div>
                <QueryLimitWarning />
                <Toaster />
              </ThemeProvider>
            </body>
          </html>
        </SessionProvider>
      </QueryProvider>
    </ClerkProvider>
  );
}
