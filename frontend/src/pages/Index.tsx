import { useState } from "react";
import { motion } from "framer-motion";
import {
  Target,
  Brain,
  TrendingUp,
  Sparkles,
  Lightbulb,
  FileSearch,
  Loader2
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { FileUpload } from "@/components/FileUpload";
import { ScoreCard } from "@/components/ScoreCard";
import { SkillsSection } from "@/components/SkillsSection";
import { RecommendationsCard } from "@/components/RecommendationsCard";
import { ConfidenceMeter } from "@/components/ConfidenceMeter";
import { toast } from "sonner";

interface AnalysisResult {
  skill_match_percentage: number;
  semantic_match_percentage: number;
  final_match_percentage: number;
  resume_skills: string[];
  common_skills: string[];
  missing_skills: string[];
  ats_recommendations: string[];
  confidence: string;
  rewrite_suggestions: string[];
}

export default function Index() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!file) {
      toast.error("Please upload a resume file");
      return;
    }
    if (!jobDescription.trim()) {
      toast.error("Please paste a job description");
      return;
    }

    setIsAnalyzing(true);

    try {
      // 1. Upload Resume
      const formData = new FormData();
      formData.append("file", file);

      const uploadResponse = await fetch("http://127.0.0.1:8000/parse-resume", {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error("Failed to parse resume");
      }

      const uploadData = await uploadResponse.json();
      const resumeText = uploadData.text_preview;

      // 2. Analyze
      const matchResponse = await fetch("http://127.0.0.1:8000/final-match", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_text: jobDescription,
        }),
      });

      if (!matchResponse.ok) {
        const err = await matchResponse.json();
        throw new Error(err.detail || "Backend error");
      }

      const resultData = await matchResponse.json();
      setResult(resultData);
      toast.success("Analysis complete!");

    } catch (error) {
      console.error(error);
      alert("Analysis failed: " + (error instanceof Error ? error.message : String(error)));
      toast.error("An error occurred during analysis. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-border/50 backdrop-blur-sm sticky top-0 z-50 bg-background/80">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3"
          >
            <div className="p-2 rounded-xl bg-primary/10 glow-primary">
              <FileSearch className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h1 className="font-heading font-bold text-xl text-foreground">ResumeAI</h1>
              <p className="text-xs text-muted-foreground">Intelligent Resume Analysis</p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Button variant="outline" className="rounded-xl">
              <Sparkles className="h-4 w-4 mr-2" />
              Pro Version
            </Button>
          </motion.div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16 space-y-6"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
            <Sparkles className="h-4 w-4" />
            <span>Powered by AI</span>
          </div>

          <h2 className="font-heading text-5xl md:text-7xl font-bold tracking-tight text-foreground">
            Land your dream job with <br />
            <span className="gradient-text">smart analysis</span>
          </h2>

          <p className="text-xl text-muted-foreground/80 max-w-2xl mx-auto leading-relaxed">
            Upload your resume, paste the job description, and get instant AI-powered insights to optimize your application.
          </p>
        </motion.div>

        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-card rounded-3xl p-8 mb-12 shadow-xl border border-border/50"
        >
          <div className="grid md:grid-cols-2 gap-10">
            <div className="space-y-4">
              <label className="text-lg font-semibold text-foreground flex items-center gap-2">
                <FileSearch className="h-5 w-5 text-primary" />
                Upload Resume
              </label>
              <FileUpload
                file={file}
                onFileSelect={setFile}
                onRemove={() => setFile(null)}
              />
            </div>

            <div className="space-y-4">
              <label className="text-lg font-semibold text-foreground flex items-center gap-2">
                <Target className="h-5 w-5 text-primary" />
                Job Description
              </label>
              <Textarea
                placeholder="Paste the full job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                className="min-h-[220px] resize-none bg-secondary/30 border-border focus:border-primary/50 text-base rounded-xl p-4 transition-all"
              />
            </div>
          </div>

          <div className="mt-8 flex justify-center">
            <Button
              size="lg"
              onClick={handleAnalyze}
              disabled={isAnalyzing || !file || !jobDescription.trim()}
              className="rounded-full px-10 h-14 text-lg font-medium shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-all duration-300"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="h-5 w-5 mr-3 animate-spin" />
                  Analyzing Resume...
                </>
              ) : (
                <>
                  <Brain className="h-5 w-5 mr-3" />
                  Start Analysis
                </>
              )}
            </Button>
          </div>
        </motion.div>

        {/* Results Section */}
        {result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="space-y-12"
          >
            {/* Confidence Badge */}
            <div className="flex justify-center scale-110">
              <ConfidenceMeter confidence={result.confidence} />
            </div>

            {/* Score Cards */}
            <div className="grid md:grid-cols-3 gap-6">
              <ScoreCard
                title="Skill Match"
                value={result.skill_match_percentage}
                icon={Target}
                color="primary"
                delay={0}
              />
              <ScoreCard
                title="Semantic Match"
                value={result.semantic_match_percentage}
                icon={Brain}
                color="info"
                delay={0.1}
              />
              <ScoreCard
                title="Overall Score"
                value={result.final_match_percentage}
                icon={TrendingUp}
                color="success"
                delay={0.2}
              />
            </div>

            {/* Skills Analysis */}
            <div className="bg-card rounded-3xl p-8 border border-border/50 shadow-sm">
              <h3 className="font-heading text-2xl font-bold mb-8 flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary/10">
                  <Brain className="h-6 w-6 text-primary" />
                </div>
                Skills Analysis
              </h3>
              <SkillsSection
                resumeSkills={result.resume_skills}
                commonSkills={result.common_skills}
                missingSkills={result.missing_skills}
              />
            </div>

            {/* Recommendations */}
            <div className="grid md:grid-cols-2 gap-8">
              <RecommendationsCard
                title="ATS Optimization Tips"
                icon={Target}
                recommendations={result.ats_recommendations}
                delay={0.3}
              />
              <RecommendationsCard
                title="Resume Improvements"
                icon={Lightbulb}
                recommendations={result.rewrite_suggestions}
                delay={0.4}
              />
            </div>
          </motion.div>
        )}

        {/* Empty State - Removed or Simplified */}
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 mt-16">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} Thamizh Resume AI • Helping candidates land their dream jobs</p>
        </div>
      </footer>
    </div>
  );
}
