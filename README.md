# Candidate Matcher

A machine learning–based candidate ranking system that matches resumes with a job description using sentence embeddings and cosine similarity.

## Features

- Match candidates with a given job description
- Rank candidates based on similarity score
- Display the Top 5 matching candidates
- View detailed candidate profiles
- Download ranked candidates as an Excel file
- Fast semantic search using precomputed embeddings

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS

### Machine Learning
- Sentence Transformers (all-MiniLM-L6-v2)
- Scikit-learn (Cosine Similarity)

### Data Processing
- Pandas
- OpenPyXL

## Project Structure

```
Candidate-Matcher/
│
├── index.html
├── style.css
├── script.js
├── README.md
│
└── backend/
    ├── app.py
   ├── generate_embedding.py
   └── requirements.txt

        
## Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/Candidate-Matcher.git
```

2. Install dependencies

```bash
pip install -r backend/requirements.txt
```

3. Place the dataset files inside the dataset folder.

Required files:
- candidates.jsonl
- candidate_embeddings.jsonl

4. Update the dataset paths inside `app.py` if required.

5. Run the backend

```bash
cd backend
python app.py
```

6. Open `index.html` using Live Server.

## How It Works

1. Recruiter enters a job description.
2. The backend generates an embedding using Sentence Transformers.
3. Cosine similarity is calculated against candidate embeddings.
4. Candidates are ranked by similarity score.
5. Top candidates are displayed on the UI.
6. Recruiters can download the ranked candidates in Excel format.

## Dependencies

- Flask
- Flask-CORS
- sentence-transformers
- scikit-learn
- pandas
- openpyxl
- torch
- numpy

## Notes

- Dataset files are not included in this repository.
- Candidate embeddings must be generated before running the application.
- The application expects the dataset to be available locally.

## Future Improvements

- Recruiter preference filters
- Advanced candidate search
- Pagination for large datasets
- Authentication and recruiter dashboard
- Deployment on cloud

## Author

Harshita Sinha
