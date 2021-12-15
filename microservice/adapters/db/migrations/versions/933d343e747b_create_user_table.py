"""create user table.

Revision ID: 933d343e747b
Revises:
Create Date: 2021-12-09 17:17:31.121338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '933d343e747b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True)
    )


def downgrade():
    op.drop_table('users')
