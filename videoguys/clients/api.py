# coding: utf-8

"""
    Video API

    Official API
"""

import os

from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from videoguys.clients.upload import UploadClient

class UploadResource(Resource):
    actions = {
        'create': {'method': 'POST', 'url': 'upload/{}'},
        'destroy': {'method': 'DELETE', 'url': 'upload/{}'},
        'retrieve': {'method': 'GET', 'url': 'upload/{}'},
        'update': {'method': 'PUT', 'url': 'upload/{}'}
    }

class ApiClient(object):

    def __init__(self, **vargs):
        if 'api_token' not in vargs:
            raise ValueError("an api_token is required for all requests")
        self.api_token = vargs['api_token']

        if 'api_host' not in vargs:
            raise ValueError("an api_host is required for all requests")

        self.api_host = "https://vev.io/api"
        if vargs['api_host'] == "vidup":
            self.api_host = "https://vidup.io/api"
        
        self.setup()

    def setup(self):
        self.api = API(
          api_root_url=self.api_host,
          params = {
            "api_token": self.api_token
          },
          headers = {
            "User-Agent": "VideoGuys/0.1.0/python"
          },
          timeout = 10,
          append_slash = False,
          json_encode_body = False
        )
        self.api.add_resource(resource_name='pair')
        self.api.add_resource(resource_name='serve')
        self.api.add_resource(resource_name='upload', resource_class=UploadResource)

    def getVideoInfo(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "video/" + code
        return self.api.serve.retrieve(path).body

    def getVideoPair(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        return self.api.pair.retrieve(code).body

    def getVideoUploads(self, **kwargs):
        return self.api.upload.retrieve('video').body

    def getVideoUpload(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "video/" + code
        return self.api.upload.retrieve(path).body

    def getUrlUploads(self, **kwargs):
        return self.api.upload.retrieve('url').body

    def getUrlUpload(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "url/" + code
        return self.api.upload.retrieve(path).body

    def getUrlUploadStatus(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "url/" + code + "/status"
        return self.api.upload.retrieve(path).body

    def newVideoUpload(self, **kwargs):
        if 'filepath' in kwargs:
            kwargs['size'] = os.path.getsize(kwargs['filepath'])
        return self.newUpload('video', **kwargs)

    def newUrlUpload(self, **kwargs):
        return self.newUpload('url', **kwargs)

    def newUpload(self, type, **kwargs):
        body_params = [
            'url',
            'size',
            'title',
            'description',
            'folder_id',
            'lite',
            'public'
        ]
        body = {}
        for key in body_params:
            if key in kwargs:
                body[key] = kwargs[key]
        return self.api.upload.create(type, body=body).body

    def deleteVideoUpload(self, code, **kwargs):
        return self.deleteUpload('video', code, **kwargs)

    def deleteUrlUpload(self, code, **kwargs):
        return self.deleteUpload('url', code, **kwargs)

    def deleteUpload(self, type, code, **kwargs):
        path = type + "/" + code
        return self.api.upload.destroy(path).body

    def updateVideoUpload(self, code, **kwargs):
        return self.updateUpload('video', code, **kwargs)

    def updateUrlUpload(self, code, **kwargs):
        return self.updateUpload('url', code, **kwargs)

    def updateUpload(self, type, code, **kwargs):
        body_params = [
            'title',
            'description',
            'folder_id',
            'lite',
            'public'
        ]
        body = {}
        for key in body_params:
            if key in kwargs:
                body[key] = kwargs[key]
        path = type + "/" + code
        return self.api.upload.update(path, body=body).body

    def uploadVideo(self, **kwargs):
        if 'filepath' not in kwargs:
            raise ValueError("invalid filepath specified")

        if 'code' in kwargs:
            video_upload = self.getVideoUpload(kwargs['code'])            
        else:
            video_upload = self.newVideoUpload(**kwargs)

        if (not video_upload
            or ('uploads' not in video_upload
                and 'upload' not in video_upload)):
            raise ValueError("invalid upload code or filepath specified")

        if 'code' in kwargs:
            video_upload = video_upload['uploads'][0]
        else:
            video_upload = video_upload['upload']

        upload_client = UploadClient(
            filepath=kwargs['filepath'],
            upload_url=video_upload['url']
        )
        
        return upload_client.start()
