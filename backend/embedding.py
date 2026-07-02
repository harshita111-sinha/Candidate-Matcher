from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

path = r"C:\Users\harsh\Documents\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\sample_candidates.json"

with open(path, "r", encoding="utf-8") as file:
    data = json.load(file)

model = SentenceTransformer("all-MiniLM-L6-v2")

job_description = """
Backend Engineer
Python
SQL
Spark
Cloud
"""

job_embedding = model.encode(job_description)

results = []

for candidate in data:

    text = candidate["profile"]["headline"] + " "

    for skill in candidate["skills"]:
        text += skill["name"] + " "

    candidate_embedding = model.encode(text)

    score = cosine_similarity(
        [job_embedding],
        [candidate_embedding]
    )[0][0]

    results.append({
        "candidate_id": candidate["candidate_id"],
        "score": score
    })

results.sort(
    key=lambda x: x["score"],
    reverse=True
)

print("\nTop 5 Candidates:\n")

for candidate in results[:5]:
    print(
        candidate["candidate_id"],
        round(float(candidate["score"]), 3)
    )