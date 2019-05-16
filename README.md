# videoguys-python-client
Official API

- API version: 0.1
- Package version: 0.1.0

## Requirements.

Python 3.5+

### Setuptools

Install via [Setuptools](https://pypi.org/project/setuptools/) (for local testing).

```sh
pip install --user --upgrade pip
pip install --user --upgrade setuptools
sudo python setup.py install --user --prefix=
```

Or

Install via [Pip](https://pypi.org/project/pip/) (easiest method).

```sh
sudo python -m pip install videoguys
```

Then import the package:
```python
import videoguys
```

## Getting Started

Please follow the installation procedure and then run the following:

```python
from __future__ import print_function

import sys
import videoguys

from pprint import pprint

api_client = videoguys.ApiClient(
  api_token="<api_key>", api_host="[vevio|vidup]"
)

try:
    pair_response = api_client.getVideoPair("<video_code>")
    pprint(pair_response)
    
    video_info = api_client.getVideoInfo("<video_code>")
    pprint(video_info)
    
    filepath = "absolute_path_to_file"
    video_upload = api_client.uploadVideo(
      filepath=filepath, # required filepath for the new video upload
      # size=size, # optional in this function, filepath will auto determine the size
      title=title, # optional title for the new video
      description=description, # optional description for the new video
      folder_id=folder_id, # optional folder_id for the new video
      lite=lite, # optional lite setting for the new video
      public=public, # optional public setting for the new video
    )
    pprint(video_upload)

    video_uploads = api_client.getVideoUploads()
    pprint(video_uploads)

    video_upload = api_client.updateVideoUpload(
      <upload_code>,
      title=title, # optional new title for the new video
      description=description, # optional new description for the new video
      folder_id=folder_id, # optional new folder_id for the new video
      lite=lite, # optional new lite setting for the new video
      public=public, # optional new public setting for the new video
    )
    pprint(video_upload)

    video_upload = api_client.getVideoUpload(<upload_code>)
    pprint(video_upload)

    deleted_video_upload = api_client.deleteVideoUpload(<upload_code>)
    pprint(deleted_video_upload)

    url = "http/https file url"
    url_upload = api_client.newUrlUpload(
      url=url, # required url for the new url upload
      title=title, # optional title for the new url
      description=description, # optional description for the new url
      folder_id=folder_id, # optional folder_id for the new url
      lite=lite, # optional lite setting for the new url
      public=public, # optional public setting for the new url
    )
    pprint(url_upload)
    
    url_uploads = api_client.getUrlUploads()
    pprint(url_uploads)

    url_upload = api_client.updateUrlUpload(
      <upload_code>,
      title=title, # optional new title for the new url
      description=description, # optional new description for the new url
      folder_id=folder_id, # optional new folder_id for the new url
      lite=lite, # optional new lite setting for the new url
      public=public, # optional new public setting for the new url
    )
    pprint(url_upload)

    url_upload = api_client.getUrlUpload(<upload_code>)
    pprint(url_upload)

    url_upload_status = api_client.getUrlUploadStatus(<upload_code>)
    pprint(url_upload_status)

    # if the url upload has been downloaded then you should clear it
      # to avoid concurrent hitting limits
    if (url_upload_status and
        'status' in url_upload_status and
        url_upload_status['status'] == "downloaded"):

        deleted_url_upload = api_client.deleteUrlUpload(<upload_code>)
        pprint(deleted_url_upload)
except ValueError as e:
    print("%s" % e)
except videoguys.ErrorWithResponse as e:
    print("%s" % e.response.body['message'])
except:
    print("Unexpected error:", sys.exc_info()[0])

```

## Documentation For Authorization

 All endpoints except /serve requires authorization.


## Author

 VideoGuys
