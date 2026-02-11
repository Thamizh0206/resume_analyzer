import { motion } from "framer-motion";
import { ProgressRing } from "@/components/ui/progress-ring";
import { LucideIcon } from "lucide-react";

interface ScoreCardProps {
  title: string;
  value: number | null;
  icon: LucideIcon;
  color?: "primary" | "success" | "warning" | "info";
  delay?: number;
}

export function ScoreCard({ title, value, icon: Icon, color = "primary", delay = 0 }: ScoreCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="glass-card rounded-2xl p-6 flex flex-col items-center gap-4"
    >
      <div className="flex items-center gap-2 text-muted-foreground">
        <Icon className="h-4 w-4" />
        <span className="text-sm font-medium">{title}</span>
      </div>
      
      {value !== null ? (
        <ProgressRing value={value} color={color} size={100} strokeWidth={6} />
      ) : (
        <div className="h-[100px] w-[100px] rounded-full border-2 border-dashed border-border flex items-center justify-center">
          <span className="text-2xl text-muted-foreground">--</span>
        </div>
      )}
    </motion.div>
  );
}
