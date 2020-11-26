"""initial revision

Revision ID: c726f33caeeb
Revises:
Create Date: 2020-11-26 00:15:03.617759

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c726f33caeeb'
down_revision = None
branch_labels = ('quetz-conda_suggest',)
depends_on = 'quetz'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'quetz_conda_suggest_metadata',
        sa.Column('version_id', sa.LargeBinary(length=16), nullable=False),
        sa.Column('data', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ['version_id'],
            ['package_versions.id'],
        ),
        sa.PrimaryKeyConstraint('version_id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quetz_conda_suggest_metadata')
    # ### end Alembic commands ###
