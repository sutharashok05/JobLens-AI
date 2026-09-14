from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.candidate_profile import CandidateProfile
from app.services.resume_parser import extract_text_from_pdf
from app.services.candidate_parser import extract_candidate_profile


router = APIRouter(
    prefix="/api/resumes",
    tags=["Resumes"],
)


UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # 1. Validate PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )

    # 2. Find or create user
    result = await db.execute(
        select(User).where(User.email == "demo@joblens.ai")
    )

    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            email="demo@joblens.ai",
            name="Demo User",
        )

        db.add(user)
        await db.flush()

    # 3. Generate unique filename
    file_id = uuid4().hex
    safe_filename = f"{file_id}.pdf"
    file_path = UPLOAD_DIR / safe_filename

    # 4. Save PDF
    file_content = await file.read()
    file_path.write_bytes(file_content)

    # 5. Extract text
    try:
        extracted_text = extract_text_from_pdf(str(file_path))

    except Exception as e:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Could not read PDF: {str(e)}",
        )

    if not extracted_text:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF.",
        )

    # 6. Profile Intelligence
    try:
        profile_data = extract_candidate_profile(
            extracted_text
        )

    except Exception as e:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Could not analyze resume: {str(e)}",
        )

    # 7. Deactivate previous resumes
    await db.execute(
        update(Resume)
        .where(Resume.user_id == user.id)
        .values(is_active=False)
    )

    # 8. Determine next resume version
    result = await db.execute(
        select(Resume.version)
        .where(Resume.user_id == user.id)
        .order_by(Resume.version.desc())
    )

    latest_version = result.scalars().first()

    next_version = (
        1 if latest_version is None else latest_version + 1
    )

    # 9. Create new resume
    resume = Resume(
        user_id=user.id,
        file_name=file.filename or "resume.pdf",
        file_path=str(file_path),
        version=next_version,
        extracted_text=extracted_text,
        is_active=True,
    )

    db.add(resume)
    await db.flush()

    # 10. Find existing candidate profile
    result = await db.execute(
        select(CandidateProfile).where(
            CandidateProfile.user_id == user.id
        )
    )

    profile = result.scalar_one_or_none()

    # 11. Create or update Profile Intelligence
    if profile is None:

        profile = CandidateProfile(
            user_id=user.id,
            resume_id=resume.id,

            # Skills
            skills=profile_data["skills"],
            core_skills=profile_data["core_skills"],
            supporting_skills=profile_data["supporting_skills"],

            # Candidate information
            education=profile_data["education"],
            experience=profile_data["experience"],
            experience_level=profile_data["experience_level"],

            # Resume information
            projects=profile_data["projects"],
            certifications=profile_data["certifications"],

            # Job-search intelligence
            preferred_roles=profile_data["preferred_roles"],
            preferred_locations=profile_data["preferred_locations"],
            preferred_work_modes=profile_data["preferred_work_modes"],
            career_keywords=profile_data["career_keywords"],

            summary=profile_data["summary"],
        )

        db.add(profile)

    else:

        # Update profile for new resume
        profile.resume_id = resume.id

        # Skills
        profile.skills = profile_data["skills"]
        profile.core_skills = profile_data["core_skills"]
        profile.supporting_skills = profile_data["supporting_skills"]

        # Candidate information
        profile.education = profile_data["education"]
        profile.experience = profile_data["experience"]
        profile.experience_level = profile_data["experience_level"]

        # Resume information
        profile.projects = profile_data["projects"]
        profile.certifications = profile_data["certifications"]

        # Job-search intelligence
        profile.preferred_roles = profile_data["preferred_roles"]
        profile.preferred_locations = profile_data["preferred_locations"]
        profile.preferred_work_modes = profile_data["preferred_work_modes"]
        profile.career_keywords = profile_data["career_keywords"]

        profile.summary = profile_data["summary"]

    # 12. Save everything
    await db.commit()

    await db.refresh(resume)
    await db.refresh(profile)

    # 13. Return Profile Intelligence
    return {
        "message": "Resume uploaded and profile intelligence created successfully",

        "resume": {
            "resume_id": resume.id,
            "version": resume.version,
            "file_name": resume.file_name,
            "text_length": len(extracted_text),
            "is_active": resume.is_active,
        },

        "profile": {
            "profile_id": profile.id,

            "skills": profile.skills,
            "core_skills": profile.core_skills,
            "supporting_skills": profile.supporting_skills,

            "experience_level": profile.experience_level,

            "preferred_roles": profile.preferred_roles,
            "preferred_locations": profile.preferred_locations,
            "preferred_work_modes": profile.preferred_work_modes,

            "career_keywords": profile.career_keywords,

            "education": profile.education,
            "experience": profile.experience,
            "projects": profile.projects,
            "certifications": profile.certifications,

            "summary": profile.summary,
        },
    }