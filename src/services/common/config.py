import os

class ConfigBase(object):
    @classmethod
    def to_dict(cls):
        d = {}
        for key in dir(cls):
            if key.isupper():
                d[key] = getattr(cls, key)

        return d

class Config(ConfigBase):
    PG_CONNECTION_URI = os.environ.get('PG_CONNECTION_URI')
    AMQP_URI = os.environ.get('AMQP_URI')
    PROCESSING_QUEUE = 'photo-processor'
    THUMBNAIL_SIZE = 320, 320
    DESTINATION_DIR = '/tpp-app-thumbs'
