import { motion } from "framer-motion";

interface SkillBadgeProps {
  skill: string;
  variant?: "default" | "success" | "warning" | "destructive";
  index?: number;
}

const variantStyles = {
  default: "bg-secondary text-foreground border-border",
  success: "bg-success/10 text-success border-success/30",
  warning: "bg-warning/10 text-warning border-warning/30",
  destructive: "bg-destructive/10 text-destructive border-destructive/30",
};

export function SkillBadge({ skill, variant = "default", index = 0 }: SkillBadgeProps) {
  return (
    <motion.span
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className={`
        inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium
        border transition-all hover:scale-105
        ${variantStyles[variant]}
      `}
    >
      {skill}
    </motion.span>
  );
}
