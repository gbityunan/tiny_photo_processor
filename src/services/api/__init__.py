import os
from flask import Flask
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from common.config import Config

app = Flask(__name__)
app.config.from_object(Config)

def _create_db_session():
    engine = create_engine(app.config.get('PG_CONNECTION_URI'),
                           convert_unicode=True)

    return scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                       bind=engine))

@app.teardown_appcontext
def _shutdown_db_session(response_or_exc):
    db_session.remove()
    return response_or_exc

db_session = _create_db_session()
ma = Marshmallow(app)

import api.views
