import json
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

path = r"C:\Users\harsh\Documents\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\candidates.jsonl"

output_file = "candidate_embeddings.jsonl"

count = 0

with open(path, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:

    for line in infile:

        candidate = json.loads(line)

        text = candidate["profile"]["headline"] + " "

        for skill in candidate["skills"]:
            text += skill["name"] + " "

        embedding = model.encode(text).tolist()

        json.dump({
            "candidate_id": candidate["candidate_id"],
            "embedding": embedding
        }, outfile)

        outfile.write("\n")

        count += 1

        if count % 1000 == 0:
            print(f"{count} candidates completed")

print("Finished!")
print("Embeddings saved in candidate_embeddings.jsonl")