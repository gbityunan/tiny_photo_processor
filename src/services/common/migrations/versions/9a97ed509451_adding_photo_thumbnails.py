"""Adding photo_thumbnails

Revision ID: 9a97ed509451
Revises: 217824308d6e
Create Date: 2019-05-10 19:16:01.531434

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9a97ed509451'
down_revision = '217824308d6e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('photo_thumbnails',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('photo_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('width', sa.SmallInteger(), nullable=False),
        sa.Column('height', sa.SmallInteger(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['photo_uuid'], ['photos.uuid'], ),
        sa.PrimaryKeyConstraint('uuid')
    )


def downgrade():
    op.drop_table('photo_thumbnails')
