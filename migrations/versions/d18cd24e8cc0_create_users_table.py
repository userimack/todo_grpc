"""create users table

Revision ID: d18cd24e8cc0
Revises:
Create Date: 2017-10-18 18:30:07.796980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd18cd24e8cc0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(30), nullable=False)
    )


def downgrade():
    op.drop_table('users')
