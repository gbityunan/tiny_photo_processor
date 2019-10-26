#! /usr/bin/env sh

export FLASK_APP=api

cd src/services
flask run --host=0.0.0.0 --port=3000
