import os
import sys
import json
import signal
import logging
from PIL import Image
from io import BytesIO
from urllib import request
from os.path import dirname, realpath
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from common.config import Config
from common.models import Photo, PhotoThumbnail
from common.photoprocessing import PhotoProcessingQueue

conf = Config.to_dict()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ppq = PhotoProcessingQueue(conf['AMQP_URI'], conf['PROCESSING_QUEUE'])

engine = create_engine(conf['PG_CONNECTION_URI'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))

def download_image(url):
    response = request.urlopen(url)
    return Image.open(BytesIO(response.read()))

def create_thumbnail(photo):
    image = download_image(photo.url)
    image.thumbnail(conf['THUMBNAIL_SIZE'], Image.ANTIALIAS)

    file_name = f'{photo.uuid}_thumb.jpg'
    target = os.path.join(conf['DESTINATION_DIR'], file_name)

    image.save(target, "JPEG", quality=90)

    width, height = image.size

    return PhotoThumbnail(photo_uuid=photo.uuid, width=width,
            height=height, url=file_name)

def process_photo(uuid):
    logger.info(f'Processing of photo {uuid} started')

    photo = db_session.query(Photo).get(uuid)

    if photo.status not in ('pending', 'failed'):
        logger.info('Skipping photo processing because status is neither '
            'pending nor failed. This may potentially indicate duplicate '
            f'messages in the queue. Photo UUID: {uuid}')
        return False

    photo.status = 'processing'
    db_session.commit()

    try:
        db_session.add(create_thumbnail(photo))
        photo.status = 'completed'
    except Exception as e:
        photo.status = 'failed'

        logger.error(f'Failed to create a thumbnail of the photo. UUID: {uuid}')
        logger.exception(e)

    db_session.commit()

    logger.info(f'Processing of photo {uuid} completed')

    return True

def listen_for_messages():
    logger.info('Waiting for incoming messages...')
    ppq.process_photos(process_photo)

def interrupt_handler(sig, frame):
    logger.info('Releasing resources and exiting...')
    db_session.remove()
    ppq.close_connection()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, interrupt_handler)
    listen_for_messages()
