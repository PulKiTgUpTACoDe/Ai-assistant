"use client";

import { SignIn } from "@clerk/nextjs";
import { useTheme } from "next-themes";
import { dark, experimental__simple } from "@clerk/themes";

export default function SignInPage() {
  const { theme, systemTheme } = useTheme();
  const currentTheme = theme === "system" ? systemTheme : theme;

  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn
        appearance={{
          baseTheme: currentTheme === "dark" ? dark : experimental__simple,
        }}
      />
    </div>
  );
}
