"use client";

import { useQuery } from "@/lib/context/query-context";
import { useEffect } from "react";
import { toast } from "sonner";

export function QueryLimitWarning() {
  const { remainingQueries, isLimitReached, queryCount } = useQuery();

  useEffect(() => {
    // Don't show anything if user hasn't made any queries
    if (queryCount === 0) return;

    if (isLimitReached) {
      toast.error("Query Limit Reached", {
        description: "Please sign in to continue using the AI assistant.",
        duration: 5000,
      });
    } else if (remainingQueries <= 2) {
      toast.warning("Query Limit Warning", {
        description: `You have ${remainingQueries} free ${
          remainingQueries === 1 ? "query" : "queries"
        } remaining. Sign in to get unlimited access.`,
        duration: 5000,
      });
    }
  }, [queryCount, isLimitReached, remainingQueries]);

  return null;
}
