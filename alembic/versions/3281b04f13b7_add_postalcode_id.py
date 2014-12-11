"""add postalcode_id

Revision ID: 3281b04f13b7
Revises: 
Create Date: 2014-12-11 11:09:39.743065

"""

# revision identifiers, used by Alembic.
revision = '3281b04f13b7'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('censusdata', sa.Column('postalcode_id', sa.Integer, sa.ForeignKey('postalcode.id')))
	op.add_column('subjectivemeasure', sa.Column('postalcode_id', sa.Integer, sa.ForeignKey('postalcode.id')))

def downgrade():
    pass
