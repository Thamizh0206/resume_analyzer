import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface RecommendationsCardProps {
  title: string;
  icon: LucideIcon;
  recommendations: string[];
  delay?: number;
}

export function RecommendationsCard({ 
  title, 
  icon: Icon, 
  recommendations,
  delay = 0 
}: RecommendationsCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="glass-card rounded-2xl p-6"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-primary/10">
          <Icon className="h-5 w-5 text-primary" />
        </div>
        <h3 className="font-heading font-semibold text-foreground">{title}</h3>
      </div>
      
      {recommendations.length > 0 ? (
        <ul className="space-y-3">
          {recommendations.map((rec, index) => (
            <motion.li
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: delay + index * 0.1 }}
              className="flex items-start gap-3 text-sm"
            >
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-secondary flex items-center justify-center text-xs font-medium text-muted-foreground">
                {index + 1}
              </span>
              <span className="text-muted-foreground leading-relaxed">{rec}</span>
            </motion.li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-muted-foreground italic">
          Upload a resume and job description to get recommendations
        </p>
      )}
    </motion.div>
  );
}
