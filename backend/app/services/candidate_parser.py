import re


KNOWN_SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "C": ["c programming"],
    "C++": ["c++"],
    "JavaScript": ["javascript"],
    "TypeScript": ["typescript", "typescript.js"],
    "React.js": ["react", "react.js"],
    "Node.js": ["node", "node.js", "nodejs"],
    "Express.js": ["express", "express.js"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "Flask": ["flask"],
    "MongoDB": ["mongodb", "mongo db"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "SQL": ["sql"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "NLP": ["nlp", "natural language processing"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "LangChain": ["langchain"],
    "LangGraph": ["langgraph"],
    "REST API": ["rest api", "restful api", "rest apis"],
}


ROLE_KEYWORDS = {
    "AI Engineer": [
        "ai engineer",
        "artificial intelligence engineer",
    ],
    "Machine Learning Engineer": [
        "machine learning engineer",
        "ml engineer",
    ],
    "NLP Engineer": [
        "nlp engineer",
        "natural language processing engineer",
    ],
    "Data Scientist": [
        "data scientist",
        "data science",
    ],
    "Python Developer": [
        "python developer",
        "python development",
    ],
    "Backend Developer": [
        "backend developer",
        "back-end developer",
        "backend engineer",
    ],
    "Full Stack Developer": [
        "full stack developer",
        "full-stack developer",
        "fullstack developer",
    ],
    "Software Developer": [
        "software developer",
        "software engineer",
    ],
    "Frontend Developer": [
        "frontend developer",
        "front-end developer",
    ],
}


LOCATION_KEYWORDS = [
    "bangalore",
    "bengaluru",
    "hyderabad",
    "pune",
    "mumbai",
    "delhi",
    "new delhi",
    "gurgaon",
    "gurugram",
    "noida",
    "chennai",
    "kolkata",
    "jaipur",
    "udaipur",
    "ahmedabad",
]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> list[str]:
    normalized = normalize_text(text)

    found_skills = []

    for skill, aliases in KNOWN_SKILLS.items():
        for alias in aliases:
            if re.search(
                rf"(?<!\w){re.escape(alias)}(?!\w)",
                normalized
            ):
                found_skills.append(skill)
                break

    return found_skills


def extract_email(text: str) -> str | None:
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    return match.group(0) if match else None


def infer_experience_level(text: str) -> str:
    normalized = normalize_text(text)

    if re.search(r"\b(fresher|fresh graduate|entry level|no experience)\b", normalized):
        return "Entry Level"

    if re.search(r"\b(0\s*[-to]*\s*1\s*years?|1\s*year)\b", normalized):
        return "Entry Level"

    if re.search(r"\b(2\s*[-to]*\s*3\s*years?)\b", normalized):
        return "Junior"

    if re.search(r"\b(3\s*[-to]*\s*5\s*years?)\b", normalized):
        return "Mid Level"

    if re.search(r"\b(5\+?\s*years?|senior)\b", normalized):
        return "Senior"

    return "Entry Level"


def infer_roles(text: str, skills: list[str]) -> list[str]:
    normalized = normalize_text(text)

    roles = []

    for role, keywords in ROLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                roles.append(role)
                break

    # Infer useful roles from technical skills when the resume
    # doesn't explicitly mention a job title.
    skill_set = set(skills)

    if "Machine Learning" in skill_set and "Machine Learning Engineer" not in roles:
        roles.append("Machine Learning Engineer")

    if "Artificial Intelligence" in skill_set and "AI Engineer" not in roles:
        roles.append("AI Engineer")

    if "Python" in skill_set and "Python Developer" not in roles:
        roles.append("Python Developer")

    if (
        "FastAPI" in skill_set
        or "Django" in skill_set
        or "Flask" in skill_set
        or "Node.js" in skill_set
    ):
        if "Backend Developer" not in roles:
            roles.append("Backend Developer")

    if (
        "React.js" in skill_set
        and (
            "Node.js" in skill_set
            or "Express.js" in skill_set
        )
    ):
        if "Full Stack Developer" not in roles:
            roles.append("Full Stack Developer")

    return roles


def infer_locations(text: str) -> list[str]:
    normalized = normalize_text(text)

    locations = []

    for location in LOCATION_KEYWORDS:
        if location in normalized:
            locations.append(location.title())

    # Keep Bengaluru as the canonical form.
    if "Bengaluru" in locations and "Bangalore" not in locations:
        locations.append("Bangalore")

    return list(dict.fromkeys(locations))


def extract_career_keywords(
    skills: list[str],
    roles: list[str],
) -> list[str]:

    keywords = []

    keywords.extend(skills)
    keywords.extend(roles)

    return list(dict.fromkeys(keywords))


def split_skill_groups(skills: list[str]) -> tuple[list[str], list[str]]:
    core_skill_names = {
        "Python",
        "Machine Learning",
        "Artificial Intelligence",
        "NLP",
        "Deep Learning",
        "Java",
        "C++",
        "JavaScript",
        "SQL",
        "React.js",
        "Node.js",
    }

    core_skills = [
        skill for skill in skills
        if skill in core_skill_names
    ]

    supporting_skills = [
        skill for skill in skills
        if skill not in core_skill_names
    ]

    return core_skills, supporting_skills


def extract_candidate_profile(text: str) -> dict:
    skills = extract_skills(text)

    core_skills, supporting_skills = split_skill_groups(
        skills
    )

    preferred_roles = infer_roles(
        text,
        skills
    )

    preferred_locations = infer_locations(
        text
    )

    experience_level = infer_experience_level(
        text
    )

    career_keywords = extract_career_keywords(
        skills,
        preferred_roles
    )

    return {
        "skills": skills,
        "core_skills": core_skills,
        "supporting_skills": supporting_skills,
        "education": [],
        "experience": [],
        "experience_level": experience_level,
        "projects": [],
        "certifications": [],
        "preferred_roles": preferred_roles,
        "preferred_locations": preferred_locations,
        "preferred_work_modes": [],
        "career_keywords": career_keywords,
        "summary": text[:1000],
        "email": extract_email(text),
        "phone": extract_phone(text),
    }