import requests
import json


class Facebook(object):
    def __init__(self, access_token, pageid):
        self.access_token = access_token
        self.pageid = pageid
    def upload(self, video_path, title, description):
        endpoint = f'https://graph-video.facebook.com/{self.pageid}/videos'
        data = {'access_token': self.access_token, 'title':str(title), 'description':str(description)}
        files = {'file': open(video_path, 'rb')}
        try:
            response = requests.post(endpoint, data=data, files=files)
            if response.json()['id']:
                return True
            else:
                return False
        except requests.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return error