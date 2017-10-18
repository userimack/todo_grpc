"""create todos table

Revision ID: c4db7f2e27bb
Revises: d18cd24e8cc0
Create Date: 2017-10-18 18:32:57.413629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4db7f2e27bb'
down_revision = 'd18cd24e8cc0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('text', sa.String(100), nullable=False),
        sa.Column('status', sa.Integer, nullable=False)
    )


def downgrade():
    op.drop_table('todos')
