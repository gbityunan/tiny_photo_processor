"""Initial

Revision ID: 217824308d6e
Revises:
Create Date: 2019-05-01 19:56:13.323862

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '217824308d6e'
down_revision = None
branch_labels = None
depends_on = None

photos_paths = ('https://storage.googleapis.com/tpp-thumbs-dev/3c7ed419-786b-4b9a-ad41-8d763a2f22e2.jpg',
    'https://storage.googleapis.com/tpp-thumbs-dev/4dee6074-0151-4ead-a86e-fd1f64587a5a.jpg',
    'https://storage.googleapis.com/tpp-thumbs-dev/6d4326d9-72d2-4565-8390-10f330193458.jpg',
    'https://storage.googleapis.com/tpp-thumbs-dev/911d59ae-1530-4080-a303-efd903cd7eea.jpg',
    'https://storage.googleapis.com/tpp-thumbs-dev/9744d3b9-0581-4018-b348-c41a0a4c4f7e.jpg',
    'https://storage.googleapis.com/tpp-thumbs-dev/b6ff653c-083f-4c20-92d5-aa5d5a8e41f5.jpg',
    'https://storage.googleapis.com/tpp-thumbs-dev/bbcc8872-7582-4522-b78a-1897ec0a9686.jpg',
    'https://storage.googleapis.com/tpp-thumbs-dev/e5668cf2-213e-47da-98c2-32b380748750.jpg',)



def upgrade():
    connection = op.get_bind()
    connection.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto')

    photos_table = op.create_table('photos',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'completed', 'processing', 'failed', name='photo_status'), server_default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('uuid'))

    op.bulk_insert(photos_table, [{'url': path} for path in photos_paths])


def downgrade():
    op.drop_table('photos')
