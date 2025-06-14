"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { PricingCard } from "@/components/pricing-card";
import { PRICING_TIERS, ANIMATION_VARIANTS } from "@/lib/constants";

export default function PricingPage() {
  const [hoveredTier, setHoveredTier] = useState<string | null>(null);

  return (
    <motion.div
      className="container py-16"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div
        className="text-center mb-12"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
          Simple, Transparent Pricing
        </h1>
        <p className="text-muted-foreground text-lg">
          Choose the plan that's right for you
        </p>
      </motion.div>

      <motion.div
        className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto"
        variants={ANIMATION_VARIANTS.container}
        initial="hidden"
        animate="show"
      >
        {PRICING_TIERS.map((tier) => (
          <PricingCard
            key={tier.id}
            tier={tier}
            isHovered={hoveredTier === tier.id}
            onHoverStart={() => setHoveredTier(tier.id)}
            onHoverEnd={() => setHoveredTier(null)}
          />
        ))}
      </motion.div>
    </motion.div>
  );
}
