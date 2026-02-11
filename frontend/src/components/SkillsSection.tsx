import { motion } from "framer-motion";
import { SkillBadge } from "@/components/SkillBadge";
import { CheckCircle, Link2, AlertCircle } from "lucide-react";

interface SkillsSectionProps {
  resumeSkills: string[];
  commonSkills: string[];
  missingSkills: string[];
}

export function SkillsSection({ resumeSkills, commonSkills, missingSkills }: SkillsSectionProps) {
  const sections = [
    {
      title: "Your Skills",
      icon: CheckCircle,
      skills: resumeSkills,
      variant: "default" as const,
      description: "Skills extracted from your resume",
    },
    {
      title: "Matching Skills",
      icon: Link2,
      skills: commonSkills,
      variant: "success" as const,
      description: "Skills that match the job requirements",
    },
    {
      title: "Skills Gap",
      icon: AlertCircle,
      skills: missingSkills,
      variant: "destructive" as const,
      description: "Skills to consider adding",
    },
  ];

  return (
    <div className="grid md:grid-cols-3 gap-6">
      {sections.map((section, sectionIndex) => (
        <motion.div
          key={section.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: sectionIndex * 0.1 }}
          className="glass-card rounded-2xl p-6"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className={`
              p-2 rounded-lg
              ${section.variant === "success" ? "bg-success/10" : ""}
              ${section.variant === "destructive" ? "bg-destructive/10" : ""}
              ${section.variant === "default" ? "bg-secondary" : ""}
            `}>
              <section.icon className={`
                h-5 w-5
                ${section.variant === "success" ? "text-success" : ""}
                ${section.variant === "destructive" ? "text-destructive" : ""}
                ${section.variant === "default" ? "text-muted-foreground" : ""}
              `} />
            </div>
            <div>
              <h3 className="font-heading font-semibold text-foreground">{section.title}</h3>
              <p className="text-xs text-muted-foreground">{section.description}</p>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-2">
            {section.skills.length > 0 ? (
              section.skills.map((skill, index) => (
                <SkillBadge 
                  key={skill} 
                  skill={skill} 
                  variant={section.variant}
                  index={index}
                />
              ))
            ) : (
              <p className="text-sm text-muted-foreground italic">
                No skills detected
              </p>
            )}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
