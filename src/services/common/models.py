from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

Base = declarative_base()

photo_status_enum = ('pending', 'completed', 'processing', 'failed')


class Photo(Base):
    __tablename__ = 'photos'

    uuid = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    url = sa.Column(sa.Text, nullable=False)
    status = sa.Column(sa.Enum(*photo_status_enum, name='photo_status'), server_default='pending', nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)


class PhotoThumbnail(Base):
    __tablename__ = 'photo_thumbnails'

    uuid = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    photo_uuid = sa.Column(UUID(as_uuid=True), sa.ForeignKey('photos.uuid'), nullable=False)
    width = sa.Column(sa.SmallInteger, nullable=False)
    height = sa.Column(sa.SmallInteger, nullable=False)
    url = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
