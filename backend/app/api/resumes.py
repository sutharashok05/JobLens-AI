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
    # ============================================================
    # 1. Validate PDF
    # ============================================================

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )

    # ============================================================
    # 2. Find or create user
    # ============================================================

    result = await db.execute(
        select(User).where(
            User.email == "demo@joblens.ai"
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            email="demo@joblens.ai",
            name="Demo User",
        )

        db.add(user)
        await db.flush()

    # ============================================================
    # 3. Generate unique filename
    # ============================================================

    file_id = uuid4().hex

    safe_filename = f"{file_id}.pdf"

    file_path = UPLOAD_DIR / safe_filename

    # ============================================================
    # 4. Save uploaded PDF
    # ============================================================

    try:
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        file_path.write_bytes(file_content)

    except HTTPException:
        raise

    except Exception as e:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Could not save uploaded file: {str(e)}",
        )

    # ============================================================
    # 5. Extract text from PDF
    # ============================================================

    try:
        extracted_text = extract_text_from_pdf(
            str(file_path)
        )

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

    # ============================================================
    # 6. Extract candidate intelligence
    #
    # Only job-relevant information should be returned by
    # candidate_parser.py.
    # ============================================================

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

    # ============================================================
    # 7. Deactivate previous resumes
    # ============================================================

    await db.execute(
        update(Resume)
        .where(
            Resume.user_id == user.id
        )
        .values(
            is_active=False
        )
    )

    # ============================================================
    # 8. Determine next resume version
    # ============================================================

    result = await db.execute(
        select(Resume.version)
        .where(
            Resume.user_id == user.id
        )
        .order_by(
            Resume.version.desc()
        )
    )

    latest_version = result.scalars().first()

    next_version = (
        1
        if latest_version is None
        else latest_version + 1
    )

    # ============================================================
    # 9. Create new Resume record
    # ============================================================

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

    # ============================================================
    # 10. Find existing CandidateProfile
    # ============================================================

    result = await db.execute(
        select(CandidateProfile)
        .where(
            CandidateProfile.user_id == user.id
        )
    )

    profile = result.scalar_one_or_none()

    # ============================================================
    # 11. Create or update CandidateProfile
    #
    # ONLY necessary job-search intelligence is stored.
    # ============================================================

    if profile is None:

        profile = CandidateProfile(
            user_id=user.id,
            resume_id=resume.id,

            # ----------------------------------------------------
            # Skills
            # ----------------------------------------------------

            skills=profile_data.get(
                "skills",
                [],
            ),

            core_skills=profile_data.get(
                "core_skills",
                [],
            ),

            supporting_skills=profile_data.get(
                "supporting_skills",
                [],
            ),

            # ----------------------------------------------------
            # Experience
            # ----------------------------------------------------

            experience_level=profile_data.get(
                "experience_level",
                "Fresher",
            ),

            # ----------------------------------------------------
            # Projects
            # ----------------------------------------------------

            projects=profile_data.get(
                "projects",
                [],
            ),

            # ----------------------------------------------------
            # Certifications
            # ----------------------------------------------------

            certifications=profile_data.get(
                "certifications",
                [],
            ),

            # ----------------------------------------------------
            # Preferred job roles
            # ----------------------------------------------------

            preferred_roles=profile_data.get(
                "preferred_roles",
                [],
            ),

            # ----------------------------------------------------
            # Search keywords
            # ----------------------------------------------------

            career_keywords=profile_data.get(
                "career_keywords",
                [],
            ),
        )

        db.add(profile)

    else:

        # --------------------------------------------------------
        # Update profile with latest resume intelligence
        # --------------------------------------------------------

        profile.resume_id = resume.id

        # --------------------------------------------------------
        # Skills
        # --------------------------------------------------------

        profile.skills = profile_data.get(
            "skills",
            [],
        )

        profile.core_skills = profile_data.get(
            "core_skills",
            [],
        )

        profile.supporting_skills = profile_data.get(
            "supporting_skills",
            [],
        )

        # --------------------------------------------------------
        # Experience level
        # --------------------------------------------------------

        profile.experience_level = profile_data.get(
            "experience_level",
            "Fresher",
        )

        # --------------------------------------------------------
        # Projects
        # --------------------------------------------------------

        profile.projects = profile_data.get(
            "projects",
            [],
        )

        # --------------------------------------------------------
        # Certifications
        # --------------------------------------------------------

        profile.certifications = profile_data.get(
            "certifications",
            [],
        )

        # --------------------------------------------------------
        # Preferred roles
        # --------------------------------------------------------

        profile.preferred_roles = profile_data.get(
            "preferred_roles",
            [],
        )

        # --------------------------------------------------------
        # Career keywords
        # --------------------------------------------------------

        profile.career_keywords = profile_data.get(
            "career_keywords",
            [],
        )

    # ============================================================
    # 12. Save database changes
    # ============================================================

    try:

        await db.commit()

    except Exception as e:

        await db.rollback()

        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Could not save resume/profile: {str(e)}",
        )

    # ============================================================
    # 13. Refresh database objects
    # ============================================================

    await db.refresh(resume)
    await db.refresh(profile)

    # ============================================================
    # 14. Return clean response
    # ============================================================

    return {
        "message": (
            "Resume uploaded and profile intelligence "
            "created successfully"
        ),

        "resume": {
            "resume_id": resume.id,
            "version": resume.version,
            "file_name": resume.file_name,
            "text_length": len(extracted_text),
            "is_active": resume.is_active,
        },

        "profile": {
            "profile_id": profile.id,

            # Skills
            "skills": profile.skills,
            "core_skills": profile.core_skills,
            "supporting_skills": profile.supporting_skills,

            # Experience
            "experience_level": profile.experience_level,

            # Projects
            "projects": profile.projects,

            # Certifications
            "certifications": profile.certifications,

            # Job-search intelligence
            "preferred_roles": profile.preferred_roles,
            "career_keywords": profile.career_keywords,
        },
    }