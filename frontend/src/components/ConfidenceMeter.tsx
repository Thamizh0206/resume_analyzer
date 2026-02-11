import { motion } from "framer-motion";
import { Shield, ShieldCheck, ShieldAlert } from "lucide-react";

interface ConfidenceMeterProps {
  confidence: string | null;
}

export function ConfidenceMeter({ confidence }: ConfidenceMeterProps) {
  const getConfidenceDetails = () => {
    if (!confidence) return { level: 0, color: "muted", label: "Pending", icon: Shield };
    
    const lower = confidence.toLowerCase();
    if (lower.includes("high") || lower.includes("strong")) {
      return { level: 3, color: "success", label: confidence, icon: ShieldCheck };
    }
    if (lower.includes("medium") || lower.includes("moderate")) {
      return { level: 2, color: "warning", label: confidence, icon: Shield };
    }
    return { level: 1, color: "destructive", label: confidence, icon: ShieldAlert };
  };

  const { level, color, label, icon: Icon } = getConfidenceDetails();

  const colorClasses = {
    success: "text-success bg-success/10 border-success/30",
    warning: "text-warning bg-warning/10 border-warning/30",
    destructive: "text-destructive bg-destructive/10 border-destructive/30",
    muted: "text-muted-foreground bg-secondary border-border",
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className={`
        inline-flex items-center gap-3 px-5 py-3 rounded-xl border
        ${colorClasses[color as keyof typeof colorClasses]}
      `}
    >
      <Icon className="h-5 w-5" />
      <div>
        <p className="text-xs uppercase tracking-wider opacity-70">Resume Strength</p>
        <p className="font-heading font-semibold">{label}</p>
      </div>
      <div className="flex gap-1 ml-2">
        {[1, 2, 3].map((i) => (
          <motion.div
            key={i}
            initial={{ scaleY: 0 }}
            animate={{ scaleY: 1 }}
            transition={{ duration: 0.3, delay: i * 0.1 }}
            className={`
              w-1.5 rounded-full origin-bottom
              ${i === 1 ? "h-3" : i === 2 ? "h-4" : "h-5"}
              ${i <= level ? `bg-current` : "bg-current/20"}
            `}
          />
        ))}
      </div>
    </motion.div>
  );
}
