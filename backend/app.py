from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend running 🚀"


@app.route("/get_jobs", methods=["GET"])
def get_jobs():
    skills_input = request.args.get("skills", "").lower()

    if not skills_input.strip():
        return jsonify({"error": "Enter skills"}), 400

    skills = [s.strip() for s in skills_input.split(",")]

    # 🔥 Skill mapping (real-world variations)
    skill_map = {
        "java": ["java", "spring", "springboot"],
        "python": ["python", "django", "flask"],
        "react": ["react", "reactjs"],
        "sql": ["sql", "mysql", "postgresql", "database"],
        "javascript": ["javascript", "js", "node", "nodejs"],
    }

    try:
        res = requests.get("https://remotive.com/api/remote-jobs", timeout=10)
        jobs = res.json().get("jobs", [])
    except Exception as e:
        return jsonify({"error": "API failed"}), 500

    filtered_jobs = []

    for job in jobs:
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        text = title + " " + description

        # 🔥 STEP 1: Only allow dev jobs
        if not any(word in title for word in ["developer", "engineer"]):
            continue

        score = 0
        matched_skills = []

        # 🔥 STEP 2: STRICT matching
        for skill in skills:
            variations = skill_map.get(skill, [skill])

            for var in variations:
                # exact word match (no fake matches)
                if re.search(rf"\b{re.escape(var)}\b", text):
                    score += 2
                    matched_skills.append(var)
                    break

        # 🔥 STEP 3: Title boost (VERY IMPORTANT)
        for skill in skills:
            if skill in title:
                score += 3

        if score >= 2:
            filtered_jobs.append({
                "id": job.get("id"),
                "title": job.get("title"),
                "company": job.get("company_name"),
                "link": job.get("url"),
                "score": score,
                "matched_skills": list(set(matched_skills))
            })

    if not filtered_jobs:
        return jsonify({"message": "No relevant jobs found. Try different skills."})

    # 🔥 Sort + limit
    filtered_jobs = sorted(filtered_jobs, key=lambda x: x["score"], reverse=True)[:25]

    return jsonify(filtered_jobs)


    if __name__ == "__main__":
     import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)