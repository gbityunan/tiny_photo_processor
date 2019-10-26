from flask import request, jsonify

from api import app, ma, db_session
from common.models import Photo
from common.photoprocessing import PhotoProcessingQueue


class PhotoSchema(ma.ModelSchema):
    class Meta:
        model = Photo

photo_schema = PhotoSchema()
photos_schema = PhotoSchema(many=True)

@app.route('/photos/pending', methods=['GET'])
def get_pending_photos():
    pending_photos = db_session.query(Photo).filter(Photo.status == 'pending')
    result = photos_schema.dump(pending_photos)
    return jsonify(result.data)

@app.route('/photos/process', methods=['PUT'])
def process_photos():
    data = request.get_json()

    photos_queued = []

    pending_photos = db_session.query(Photo).filter(Photo.uuid.in_(data))
    ppq = PhotoProcessingQueue(app.config['AMQP_URI'], app.config['PROCESSING_QUEUE'])

    for photo in pending_photos:
        ppq.submit_photo(str(photo.uuid))

        photos_queued.append({
            'uuid': photo.uuid,
            'url': photo.url,
            'status': photo.status
        })

    ppq.close_connection()

    return jsonify({ 'photos_queued': photos_queued, 'photos_queued_count': len(photos_queued) })
