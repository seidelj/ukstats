"""convert to string

Revision ID: 990b3cccdc7
Revises: 1fe606a0a099
Create Date: 2014-12-15 14:10:44.134886

"""

# revision identifiers, used by Alembic.
revision = '990b3cccdc7'
down_revision = '1fe606a0a099'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('postalcode', sa.Column('reference_area', sa.String))


def downgrade():
    pass
