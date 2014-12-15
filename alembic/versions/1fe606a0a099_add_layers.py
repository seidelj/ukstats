"""add layers

Revision ID: 1fe606a0a099
Revises: 1dc42fe4c20f
Create Date: 2014-12-12 15:34:34.185596

"""

# revision identifiers, used by Alembic.
revision = '1fe606a0a099'
down_revision = '1dc42fe4c20f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('censusfields', sa.Column('layer', sa.String))


def downgrade():
    pass
