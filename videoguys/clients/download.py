# coding: utf-8

"""
    Video API

    Official API
"""

import urllib.request

class DownloadClient(object):

    def __init__(self, **vargs):
        if 'download_url' not in vargs:
            raise ValueError("an download_url is required for all requests")
        self.download_url = vargs['download_url']

        if 'filepath' in vargs:
            self.filepath = vargs['filepath'];

    def setfilepath(self, filepath):
        self.filepath = filepath

    def start(self):
        if not self.filepath:
            raise ValueError("file path required to start")
        return urllib.request.urlretrieve(self.download_url, self.filepath);
