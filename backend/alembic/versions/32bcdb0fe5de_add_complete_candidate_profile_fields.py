"""add complete candidate profile fields

Revision ID: 32bcdb0fe5de
Revises: 49de57290a8d
Create Date: 2026-09-14
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "32bcdb0fe5de"
down_revision = "49de57290a8d"
branch_labels = None
depends_on = None


def upgrade():
    # ---------------------------------------------------------
    # Add new fields safely.
    #
    # Existing candidate_profiles rows already exist, so
    # NOT NULL columns need temporary server defaults.
    # ---------------------------------------------------------

    op.add_column(
        "candidate_profiles",
        sa.Column(
            "email",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column(
            "phone",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column(
            "links",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column(
            "achievements",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column(
            "courses",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column(
            "preferred_employment_types",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column(
            "work_preferences",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::json"),
        ),
    )

    # ---------------------------------------------------------
    # Remove server defaults after existing rows are populated.
    #
    # Future application inserts will provide these values
    # through the SQLAlchemy model/application.
    # ---------------------------------------------------------

    op.alter_column(
        "candidate_profiles",
        "email",
        server_default=None,
    )

    op.alter_column(
        "candidate_profiles",
        "phone",
        server_default=None,
    )

    op.alter_column(
        "candidate_profiles",
        "links",
        server_default=None,
    )

    op.alter_column(
        "candidate_profiles",
        "achievements",
        server_default=None,
    )

    op.alter_column(
        "candidate_profiles",
        "courses",
        server_default=None,
    )

    op.alter_column(
        "candidate_profiles",
        "preferred_employment_types",
        server_default=None,
    )

    op.alter_column(
        "candidate_profiles",
        "work_preferences",
        server_default=None,
    )


def downgrade():
    op.drop_column(
        "candidate_profiles",
        "work_preferences",
    )

    op.drop_column(
        "candidate_profiles",
        "preferred_employment_types",
    )

    op.drop_column(
        "candidate_profiles",
        "courses",
    )

    op.drop_column(
        "candidate_profiles",
        "achievements",
    )

    op.drop_column(
        "candidate_profiles",
        "links",
    )

    op.drop_column(
        "candidate_profiles",
        "phone",
    )

    op.drop_column(
        "candidate_profiles",
        "email",
    )