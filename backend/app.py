from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from flask import send_file
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

import pandas as pd
from io import BytesIO


latest_results = []

app = Flask(__name__)
CORS(app)
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load dataset once

embedding_path = r"C:\Users\harsh\Documents\redrob hackathon\dataset\candidate_embeddings.jsonl"

candidate_embeddings = []

with open(embedding_path, "r", encoding="utf-8") as file:
    for line in file:
        candidate_embeddings.append(json.loads(line))

print(f"Loaded {len(candidate_embeddings)} embeddings.")


candidate_profiles = {}

profile_path = r"C:\Users\harsh\Documents\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\candidates.jsonl"

with open(profile_path, "r", encoding="utf-8") as file:
    for line in file:
        candidate = json.loads(line)
        candidate_profiles[candidate["candidate_id"]] = candidate

print(f"Loaded {len(candidate_profiles)} profiles.")

@app.route("/")
def home():
    return "Redrob Candidate Matcher Backend Running"


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    job_description = data.get("job_description", "")

    recruiter_preferences = data.get("preferences", [])

    print("\n========== NEW REQUEST ==========")
    print("Job Description:")
    print(job_description)

    print("\nRecruiter Preferences:")
    print(recruiter_preferences)

    results = []

    print("Generating Job Embedding...")

    job_embedding = model.encode(job_description)

    for candidate in candidate_embeddings:

        score = cosine_similarity(
            [job_embedding],
            [candidate["embedding"]]
        )[0][0]

        results.append({
            "candidate_id": candidate["candidate_id"],
            "candidate": candidate_profiles[candidate["candidate_id"]],
            "score": float(score)
        })
    results.sort(
        key = lambda x : x["score"],
        reverse = True
    )

    # Add rank
    for i, candidate in enumerate(results):
        candidate["rank"] = i + 1

    # Create DataFrame
    df = pd.DataFrame(results)

    # Convert score to percentage
    df["score"] = (df["score"] * 100).round(2)

    # Keep only required columns
    df = df[["rank", "candidate_id", "score"]]

    # Rename columns
    df.columns = ["Rank", "Candidate ID", "Match %"]

    #Save Excel
    #df.to_excel("ranked_candidates.xlsx", index=False)

    global latest_results
    latest_results = results


    return jsonify(results[:5])

@app.route("/download")
def download():

    global latest_results

    if not latest_results:
        return "No ranking available. Analyze candidates first.", 400

    df = pd.DataFrame(latest_results[:1000])

    df["score"] = (df["score"] * 100).round(2)

    df.insert(0, "Rank", range(1, len(df) + 1))

    df = df[["Rank", "candidate_id", "score"]]

    df.columns = ["Rank", "Candidate ID", "Match %"]

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="Top_Candidates.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    app.run(debug=True)

