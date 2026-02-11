import { motion } from "framer-motion";

interface ProgressRingProps {
  value: number;
  size?: number;
  strokeWidth?: number;
  color?: "primary" | "success" | "warning" | "info";
}

const colorMap = {
  primary: "hsl(var(--primary))",
  success: "hsl(var(--success))",
  warning: "hsl(var(--warning))",
  info: "hsl(var(--info))",
};

export function ProgressRing({
  value,
  size = 120,
  strokeWidth = 8,
  color = "primary"
}: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (value / 100) * circumference;
  const strokeColor = colorMap[color];

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="hsl(var(--muted))"
          strokeWidth={strokeWidth}
          strokeOpacity={0.3}
        />
        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          style={{
            filter: `drop-shadow(0 0 4px ${strokeColor})`,
          }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <motion.span
          className="text-2xl font-bold font-heading text-foreground"
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          {value}%
        </motion.span>
      </div>
    </div>
  );
}
