"""add areadid

Revision ID: 2bc786d068f0
Revises: 3281b04f13b7
Create Date: 2014-12-12 13:38:55.844137

"""

# revision identifiers, used by Alembic.
revision = '2bc786d068f0'
down_revision = '3281b04f13b7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('postalcode', sa.Column('areaid', sa.String))


def downgrade():
    pass
