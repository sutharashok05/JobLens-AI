from app.services.candidate_parser import extract_candidate_profile


sample_resume = """
Ashok Suthar
Full Stack Developer

Skills:
Python, JavaScript, React, Node.js, FastAPI,
PostgreSQL, MongoDB, Machine Learning, NLP

Education:
Bachelor of Technology in Computer Science

Projects:
JobLens AI
AI Expense Tracker
"""


profile = extract_candidate_profile(sample_resume)

print(profile)