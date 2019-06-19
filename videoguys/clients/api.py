# coding: utf-8

"""
    Video API

    Official API
"""

import os

from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from simple_rest_client.exceptions import ErrorWithResponse
from videoguys.clients.upload import UploadClient
from videoguys.clients.download import DownloadClient

class UploadResource(Resource):
    actions = {
        'create': {'method': 'POST', 'url': 'upload/{}'},
        'destroy': {'method': 'DELETE', 'url': 'upload/{}'},
        'retrieve': {'method': 'GET', 'url': 'upload/{}'},
        'update': {'method': 'PUT', 'url': 'upload/{}'}
    }

class DownloadResource(Resource):
    actions = {
        'retrieve': {'method': 'POST', 'url': 'serve/video/{}'}
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
        self.api.add_resource(resource_name='download', resource_class=DownloadResource)

    def fetchResource(self, **kwargs):
        if 'resource' not in kwargs:
            raise ValueError("resource must be defined")
        if 'method' not in kwargs:
            raise ValueError("method must be defined")
        if 'params' not in kwargs:
            raise ValueError("params must be defined")
        if 'body' not in kwargs:
            kwargs['body'] = {}
        try:
            response = getattr(getattr(self.api, kwargs['resource']), kwargs['method'])(kwargs['params'],body=kwargs['body'])
        except ErrorWithResponse as e:
            response = e.response
        except:
            raise Error("unexpected error occurred")

        return response;

    def getVideoDownload(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        return self.fetchResource(resource='download',method='retrieve',params=code).body

    def getVideoInfo(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "video/" + code
        return self.fetchResource(resource='serve',method='retrieve',params=path).body

    def getVideoPair(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        return self.fetchResource(resource='pair',method='retrieve',params=code).body

    def getVideoUploads(self, **kwargs):
        return self.fetchResource(resource='upload',method='retrieve',params='video').body

    def getVideoUpload(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "video/" + code
        return self.fetchResource(resource='upload',method='retrieve',params=path).body

    def getUrlUploads(self, **kwargs):
        return self.fetchResource(resource='upload',method='retrieve',params='url').body

    def getUrlUpload(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "url/" + code
        return self.fetchResource(resource='upload',method='retrieve',params=path).body

    def getUrlUploadStatus(self, code, **kwargs):
        if code is None:
            raise ValueError("code must be defined")
        path = "url/" + code + "/status"
        return self.fetchResource(resource='upload',method='retrieve',params=path).body

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
        return self.fetchResource(resource='upload',method='create',params=type,body=body).body

    def deleteVideoUpload(self, code, **kwargs):
        return self.deleteUpload('video', code, **kwargs)

    def deleteUrlUpload(self, code, **kwargs):
        return self.deleteUpload('url', code, **kwargs)

    def deleteUpload(self, type, code, **kwargs):
        path = type + "/" + code
        return self.fetchResource(resource='upload',method='destroy',params=path).body

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
        return self.fetchResource(resource='upload',method='update',params=path,body=body).body

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

    def downloadVideo(self, **kwargs):
        if 'filepath' not in kwargs:
            raise ValueError("invalid filepath specified")

        if 'code' not in kwargs:
            raise ValueError("invalid code specified")
        video_download = self.getVideoDownload(kwargs['code'])

        if not video_download:
            raise ValueError("invalid download code specified")

        if 'deleted' in video_download and video_download['deleted']:
            raise ValueError("video specified is not available")

        if 'qualities' not in video_download:
            raise ValueError("no video qualities available")

        video_qualities = [*video_download['qualities']]
        video_qualities.sort(reverse=True, key=lambda elem: int(elem[:-1]))
        
        download_url = video_download['qualities'][video_qualities[0]]

        download_client = DownloadClient(
            filepath=kwargs['filepath'],
            download_url=download_url
        )
        
        return download_client.start()
