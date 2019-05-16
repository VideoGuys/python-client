# coding: utf-8

"""
    Video API

    Official API
"""

import os
import math

from simple_rest_client.api import API
from simple_rest_client.resource import Resource

def chunks(file, chunksize=1024*1024*10):
        while True:
            chunk = file.read(chunksize)
            if not chunk:
                break
            yield chunk

class UpstreamResource(Resource):
    actions = {
        'upload': {'method': 'POST', 'url': ''},
        'completed': {'method': 'POST', 'url': 'completed'}
    }

class UploadClient(object):

    def __init__(self, **vargs):
        if 'upload_url' not in vargs:
            raise ValueError("an upload_url is required for all requests")
        self.upload_url = vargs['upload_url']

        if 'filepath' in vargs:
            self.filepath = vargs['filepath'];

        self.setup()

    def setup(self):
        self.upload = API(
          api_root_url=self.upload_url,
          headers = {
            "User-Agent": "VideoGuys/0.1.0/python"
          },
          timeout = 120,
          append_slash = False,
          json_encode_body = False
        )
        self.upload.add_resource(resource_name='upstream', resource_class=UpstreamResource)

    def complete(self):
        return self.upload.upstream.completed()

    def setfilepath(self, filepath):
        self.filepath = filepath

    def start(self):
        if not self.filepath:
            raise ValueError("file path required to start")

        chunkpartsize = 1024*1024*10
        totalfilesize = os.path.getsize(self.filepath)
        totalfileparts = math.ceil(totalfilesize/chunkpartsize)

        i = 0        
        file = open(self.filepath, 'rb')
        for chunk in chunks(file, chunkpartsize):
            body = {
                "qqpartindex": i,
                "qqtotalparts": totalfileparts,
                "qqtotalfilesize": totalfilesize
            }
            files = { 'qqfile': chunk }
            upload_response = self.upload.upstream.upload(body=body, files=files)
            if (not upload_response or
                not upload_response.body or
                not upload_response.body['success']):
                raise ValueError("invalid response from upload server, aborting upload")

            i += 1
        
        return self.complete().body['video']
