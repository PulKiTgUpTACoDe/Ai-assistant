"use client";

import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import { motion } from "framer-motion";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { PricingTier } from "@/lib/types";
import { cn } from "@/lib/utils";

interface PricingCardProps {
  tier: PricingTier;
  isHovered: boolean;
  onHoverStart: () => void;
  onHoverEnd: () => void;
}

export function PricingCard({
  tier,
  isHovered,
  onHoverStart,
  onHoverEnd,
}: PricingCardProps) {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 },
      }}
      className={cn(
        "rounded-lg border p-8 flex flex-col transition-all duration-300",
        tier.isPopular && "relative bg-primary/5",
        isHovered && "scale-105 shadow-lg"
      )}
      onHoverStart={onHoverStart}
      onHoverEnd={onHoverEnd}
    >
      {tier.isPopular && (
        <motion.div
          className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-4 py-1 rounded-full text-sm"
          whileHover={{ scale: 1.1 }}
          transition={{ type: "spring", stiffness: 400, damping: 10 }}
        >
          Most Popular
        </motion.div>
      )}

      <h2 className="text-2xl font-bold mb-4">{tier.name}</h2>
      <div className="text-3xl font-bold mb-6">
        {tier.price}
        {tier.price !== "Custom" && (
          <span className="text-lg font-normal text-muted-foreground">
            /month
          </span>
        )}
      </div>

      <ul className="space-y-4 mb-8 flex-grow">
        {tier.features.map((feature, index) => (
          <motion.li
            key={index}
            className="flex items-center gap-2"
            whileHover={{ x: 5 }}
            transition={{ type: "spring", stiffness: 400, damping: 10 }}
          >
            <Check className="h-5 w-5 text-green-500" />
            <span>{feature}</span>
          </motion.li>
        ))}
      </ul>

      <HoverCard>
        <HoverCardTrigger asChild>
          <Button
            variant={tier.buttonVariant}
            className="w-full group relative overflow-hidden"
          >
            <span className="relative z-10">{tier.buttonText}</span>
            <motion.div
              className={cn(
                "absolute inset-0",
                tier.buttonVariant === "default"
                  ? "bg-white/20"
                  : "bg-primary/10"
              )}
              initial={{ x: "-100%" }}
              whileHover={{ x: 0 }}
              transition={{ duration: 0.3 }}
            />
          </Button>
        </HoverCardTrigger>
        <HoverCardContent className="w-80">
          <div className="space-y-2">
            <h4 className="font-semibold">{tier.hoverCardContent.title}</h4>
            <p className="text-sm text-muted-foreground">
              {tier.hoverCardContent.description}
            </p>
          </div>
        </HoverCardContent>
      </HoverCard>
    </motion.div>
  );
}
