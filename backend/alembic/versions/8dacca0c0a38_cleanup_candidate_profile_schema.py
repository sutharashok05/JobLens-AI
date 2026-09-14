"""cleanup_candidate_profile_schema

Revision ID: 8dacca0c0a38
Revises: 32bcdb0fe5de
Create Date: 2026-09-14 17:49:53.419867

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8dacca0c0a38"
down_revision: Union[str, Sequence[str], None] = "32bcdb0fe5de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove obsolete candidate profile columns."""

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS email'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS phone'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS summary'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS education'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS experience'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS preferred_locations'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS preferred_work_modes'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS links'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS achievements'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS courses'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS preferred_employment_types'
    )

    op.execute(
        'ALTER TABLE candidate_profiles DROP COLUMN IF EXISTS work_preferences'
    )


def downgrade() -> None:
    pass