"""add layers

Revision ID: 1dc42fe4c20f
Revises: 2bc786d068f0
Create Date: 2014-12-12 13:46:37.636525

"""

# revision identifiers, used by Alembic.
revision = '1dc42fe4c20f'
down_revision = '2bc786d068f0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('postalcode', sa.Column('llsoa', sa.String))
	op.add_column('postalcode', sa.Column('mlsoa', sa.String))
	op.drop_column('postalcode', 'areaid')


def downgrade():
    pass
