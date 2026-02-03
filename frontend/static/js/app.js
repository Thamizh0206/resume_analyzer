async function analyzeResume() {
    const fileInput = document.getElementById("resumeFile");
    const jobText = document.getElementById("jobDescription").value;

    if (!fileInput.files.length) {
        alert("Please upload a resume file");
        return;
    }

    if (!jobText.trim()) {
        alert("Please paste a job description");
        return;
    }

    // -------- Upload Resume --------
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const resumeResponse = await fetch("/parse-resume", {
        method: "POST",
        body: formData
    });

    const resumeData = await resumeResponse.json();

    // -------- Final Match --------
    const matchResponse = await fetch("/final-match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            resume_text: resumeData.text_preview,
            job_text: jobText
        })
    });

    const data = await matchResponse.json();

    // -------- Update UI --------
    document.getElementById("skillMatch").innerText =
        data.skill_match_percentage + "%";

    document.getElementById("semanticMatch").innerText =
        data.semantic_match_percentage + "%";

    document.getElementById("finalMatch").innerText =
        data.final_match_percentage + "%";

    document.getElementById("resumeSkills").innerText =
        JSON.stringify(data.resume_skills, null, 2);

    document.getElementById("commonSkills").innerText =
        JSON.stringify(data.common_skills, null, 2);

    document.getElementById("missingSkills").innerText =
        JSON.stringify(data.missing_skills, null, 2);

    document.getElementById("atsTips").innerText =
        JSON.stringify(data.ats_recommendations, null, 2);

    document.getElementById("confidence").innerText = data.confidence;

    document.getElementById("rewriteTips").innerText =
        JSON.stringify(data.rewrite_suggestions, null, 2);
}
