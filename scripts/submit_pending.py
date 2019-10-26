#!/usr/bin/env python

# Very barebones script to submit all pending photos for processing
# Requires requests

import requests
import json

photos = json.loads(requests.get('http://localhost:3000/photos/pending').content)
requests.put('http://localhost:3000/photos/process', json=[photo['uuid'] for photo in photos])
