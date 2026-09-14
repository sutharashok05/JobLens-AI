# 🔎 JobLens AI

> **Your resume. Your skills. Your next opportunity.**

**JobLens AI** is a full-stack, resume-based intelligent job discovery platform that helps candidates discover relevant job opportunities based on their resume, skills, experience level, preferred roles, and search intent.

The platform processes a candidate's resume, creates a structured candidate profile, generates personalized search queries, fetches live jobs from multiple sources, and then **normalizes, verifies, deduplicates, matches, and ranks** the results.

---

## 🌐 Live Demo

🚀 **Try JobLens AI:**

[Open JobLens AI](https://joblens-frontend.onrender.com/)

### ⚙️ Backend

[Open Backend API](https://joblens-backend-new.onrender.com/)

### 📚 Swagger API Documentation

[Open Swagger Docs](https://joblens-backend-new.onrender.com/docs)

### 💻 GitHub

[JobLens AI Repository](https://github.com/sutharashok05/JobLens-AI)

---

## 📌 Problem Statement

Finding a suitable job often requires candidates to search repeatedly across different platforms using different combinations of:

- Job roles
- Skills
- Locations
- Experience levels
- Keywords

This creates several problems:

- Repetitive job searches
- Irrelevant job results
- Duplicate job listings
- Multiple job sources
- Difficult manual comparison
- Time-consuming job filtering

JobLens AI aims to simplify this process by using the **candidate's resume as the foundation for personalized job discovery**.

---

## 💡 Solution

JobLens AI converts a resume into a structured candidate profile and uses that profile together with the user's search query to discover more relevant opportunities.

```text
Resume
   ↓
Resume Parsing
   ↓
Candidate Profile
   ↓
Search Intent
   ↓
Personalized Search Queries
   ↓
Live Job Sources
   ↓
Normalization
   ↓
Verification
   ↓
Deduplication
   ↓
Resume-Job Matching
   ↓
Intelligent Ranking
   ↓
Relevant Jobs
```

---

# ✨ Features

## 📄 Resume Upload & Parsing

- Upload PDF resume
- Extract resume information
- Create structured candidate profile
- Maintain active resume
- Support replacing/updating the active resume

---

## 👤 Candidate Profile

The system extracts and stores relevant information such as:

- Skills
- Core Skills
- Supporting Skills
- Experience Level
- Projects
- Certifications
- Preferred Roles
- Career Keywords

---

## 🎯 Search Intent

The user's search query is analyzed to identify relevant information such as:

- Job role
- Location
- Experience level
- Search keywords

---

## 🧠 Personalized Search

The candidate profile and search intent are combined to generate personalized job-search queries.

---

## 🌐 Live Job Discovery

Currently enabled job sources:

- **Adzuna**
- **Google Jobs via SerpAPI**

---

## ⚡ Parallel Searching

Multiple personalized queries are searched across job providers asynchronously.

---

## 🧹 Job Normalization

Different provider responses are converted into a common job format.

---

## ✅ Job Verification

Discovered jobs pass through a verification stage before final processing.

---

## ♻️ Job Deduplication

Duplicate listings from different sources are removed.

---

## 🎯 Resume-to-Job Matching

Jobs are matched against the candidate profile using relevant candidate information.

---

## 🏆 Intelligent Ranking

Matched jobs are ranked so that more relevant opportunities can appear first.

---

## 💾 Persistent Search Results

Frontend job results are maintained using:

- Redux Toolkit
- React Redux
- localStorage

---

## 📱 Responsive UI

The application provides a responsive web interface with dedicated pages for:

- Dashboard
- Resume
- Profile
- Jobs
- Job Details

---

# 🧠 System Architecture

```text
                         USER
                          │
                          ▼
                ┌──────────────────┐
                │   React + Vite   │
                │    Frontend      │
                └────────┬─────────┘
                         │
                         │ REST API
                         ▼
                ┌──────────────────┐
                │     FastAPI      │
                │     Backend      │
                └────────┬─────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     Resume          Search         PostgreSQL
    Processing       Planning
          │              │
          ▼              ▼
 Candidate Profile   Personalized
                     Search Queries
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
              Adzuna        Google Jobs
                            via SerpAPI
                 │                 │
                 └────────┬────────┘
                          ▼
                       Raw Jobs
                          │
                          ▼
                    Normalization
                          │
                          ▼
                     Verification
                          │
                          ▼
                    Deduplication
                          │
                          ▼
                  Resume Matching
                          │
                          ▼
                  Intelligent Ranking
                          │
                          ▼
                     Final Jobs
```

---

# 🔄 Complete Workflow

## 1. Resume Upload

The user uploads a PDF resume.

```text
PDF Resume
    ↓
Resume Upload API
    ↓
Resume Text Extraction
```

---

## 2. Candidate Profile Creation

The extracted resume text is processed to create a structured candidate profile.

```text
Resume Text
    ↓
Candidate Parser
    ↓
Candidate Profile
```

---

## 3. Search Query

The user enters a job-search query.

Example:

```text
Python Developer in Bangalore
```

---

## 4. Search Intent

The system analyzes the query and extracts relevant search information.

```text
Search Query
    ↓
Search Intent
    ├── Role
    ├── Location
    ├── Experience
    └── Keywords
```

---

## 5. Personalized Search Plan

The candidate profile is combined with the search intent.

```text
Candidate Profile
        +
Search Intent
        ↓
Personalized Search Plan
```

---

## 6. Job Discovery

The generated queries are searched across enabled providers.

```text
Personalized Queries
        │
        ├──────────────┐
        ▼              ▼
     Adzuna       Google Jobs
                  via SerpAPI
        │              │
        └───────┬──────┘
                ▼
             Raw Jobs
```

---

## 7. Job Processing

```text
Raw Jobs
   ↓
Normalization
   ↓
Verification
   ↓
Deduplication
   ↓
Matching
   ↓
Ranking
```

---

## 8. Final Results

The frontend displays the processed and ranked job opportunities.

---

# 🔎 Job Search Pipeline

The main search pipeline is:

```text
Search Request
      ↓
Search Intent
      ↓
Candidate Profile
      ↓
Personalized Search Plan
      ↓
Multiple Search Queries
      ↓
Adzuna + Google Jobs
      ↓
Raw Job Results
      ↓
Job Normalization
      ↓
Job Verification
      ↓
Job Deduplication
      ↓
Resume-Job Matching
      ↓
Intelligent Ranking
      ↓
Final Ranked Jobs
```

---

# 👤 Candidate Profile

JobLens AI keeps the candidate profile focused on information useful for job discovery.

### Profile Fields

```text
skills
core_skills
supporting_skills
experience_level
projects
certifications
preferred_roles
career_keywords
```

The profile is associated with the active resume and user.

---

# 🌐 Job Providers

## Adzuna

Adzuna is used as one of the live job sources.

The provider can return information including:

- Job title
- Company
- Location
- Description
- Salary information when available
- Employment information
- Job/application URL

---

## Google Jobs via SerpAPI

Google Jobs is accessed through SerpAPI.

The provider can return:

- Job title
- Company
- Location
- Description
- Job URL
- Application options
- Employment information

---

# ⚡ Provider Architecture

Job providers follow a common provider architecture.

```text
                Provider Registry
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
          Adzuna             Google Jobs
                              SerpAPI
             │                   │
             └─────────┬─────────┘
                       ▼
                   Job Results
```

Additional providers can be integrated in the future without changing the overall search pipeline.

---

# 🧹 Job Processing

Every discovered job goes through multiple processing stages.

### Normalization

Converts different provider formats into a common job structure.

### Verification

Processes job listings through the verification layer.

### Deduplication

Removes duplicate job listings collected from different providers.

### Matching

Compares jobs with candidate information.

### Ranking

Orders the final jobs based on relevance.

---

# 🎯 Resume-Job Matching

Job matching uses the candidate profile as the basis for relevance.

```text
Candidate Profile
      │
      ├── Skills
      ├── Core Skills
      ├── Supporting Skills
      ├── Experience Level
      ├── Preferred Roles
      ├── Career Keywords
      ├── Projects
      └── Certifications
              │
              ▼
         Job Matching
              │
              ▼
         Matched Jobs
```

---

# 🏆 Intelligent Ranking

After matching, jobs are passed to the ranking service.

```text
Matched Jobs
     ↓
Job Ranker
     ↓
Ranked Opportunities
```

This helps surface more relevant opportunities earlier in the results.

---

# 💻 Frontend

The frontend is built with **React + Vite**.

### Main Pages

```text
/
├── Dashboard
├── Resume
├── Profile
├── Jobs
└── Jobs/:id
```

### Frontend Responsibilities

- Resume upload interface
- Candidate profile display
- Job search interface
- Job listing display
- Job details
- Navigation
- Redux state management
- Persistent job results

---

# ⚙️ Backend

The backend is built using **FastAPI**.

### Main Responsibilities

- Resume upload
- Resume parsing
- Candidate profile management
- Search intent processing
- Search planning
- Personalized queries
- Job provider integration
- Job normalization
- Job verification
- Job deduplication
- Job matching
- Job ranking

---

# 🗄️ Database

JobLens AI uses **PostgreSQL** for persistent application data.

### Main Entities

```text
Users
   │
   ├── Resumes
   │
   └── Candidate Profiles
```

Database migrations are managed using **Alembic**.

---

# 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/resumes/upload` | Upload and process resume |
| `GET` | `/api/profile` | Get candidate profile |
| `POST` | `/api/search/intent` | Analyze search intent |
| `POST` | `/api/search/plan` | Create search plan |
| `POST` | `/api/search/personalized-plan` | Generate personalized queries |
| `POST` | `/api/search/jobs` | Search, match and rank jobs |

---

# 🛠️ Tech Stack

## Frontend

- React.js
- Vite
- React Router
- Redux Toolkit
- React Redux
- Axios
- Tailwind CSS

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- HTTPX
- Alembic

## Database

- PostgreSQL

## APIs

- Adzuna API
- SerpAPI / Google Jobs

## Deployment

- Render

---

# 📁 Project Structure

```text
joblens-ai/
│
├── backend/
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── providers/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── uploads/
│   │   └── resumes/
│   │
│   ├── .env.example
│   ├── alembic.ini
│   ├── requirements.txt
│   └── tests/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   └── store/
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── print_structure.py
└── project-structure.txt
```

---

# ⚙️ Local Setup

## Prerequisites

- Python 3.x
- Node.js
- npm
- PostgreSQL
- Git

---

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

### Backend

```text
http://127.0.0.1:8000
```

### Swagger

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

### Frontend

```text
http://localhost:5173
```

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=your_postgresql_database_url

ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

SERPAPI_KEY=your_serpapi_key
```

> ⚠️ Never commit `.env` files, API keys, database passwords, or other secrets to GitHub.

---

# 🧪 Testing

The backend contains tests/utilities for important project components:

```text
test_parser.py
test_matcher.py
test_ranker.py
test_serpapi.py
```

These help validate:

- Resume parsing
- Job matching
- Job ranking
- SerpAPI integration

---

# 📦 Production Build

Build the frontend using:

```bash
cd frontend

npm run build
```

The production build is generated inside:

```text
frontend/dist/
```

---

# ☁️ Deployment

JobLens AI is deployed using **Render**.

### Frontend

https://joblens-frontend.onrender.com/

### Backend

https://joblens-backend-new.onrender.com/

### API Documentation

https://joblens-backend-new.onrender.com/docs

---

# 🔒 Security

Sensitive configuration is handled using environment variables.

### Important Secrets

```text
DATABASE_URL
ADZUNA_APP_ID
ADZUNA_APP_KEY
SERPAPI_KEY
```

These should not be exposed in the source code or committed to GitHub.

---

# 🔮 Future Improvements

- 🔐 User authentication
- ⭐ Saved jobs
- 📋 Application tracking
- 🔔 Personalized job alerts
- 🧠 Advanced semantic matching
- 📊 Job search analytics
- 🎯 Skill-gap analysis
- 🌐 Additional verified job sources

---

# 👨‍💻 Author

## Ashok Suthar

**Computer Science & Engineering Undergraduate**

### Interested In

- Full Stack Development
- Python
- Machine Learning
- Artificial Intelligence
- Data Analysis
- Backend Development

---

# 🔗 Links

| Resource | Link |
|---|---|
| 🚀 Live Demo | https://joblens-frontend.onrender.com/ |
| 💻 GitHub | https://github.com/sutharashok05/JobLens-AI |
| ⚙️ Backend | https://joblens-backend-new.onrender.com/ |
| 📚 Swagger | https://joblens-backend-new.onrender.com/docs |

---

# ⭐ Support

If you find **JobLens AI** useful, please consider giving the repository a ⭐.

---

<p align="center">

**🔎 JobLens AI — Discover Jobs That Match You.**

Built with ❤️ by **Ashok Suthar**

</p>
