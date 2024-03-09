import requests
import json
import time, os


class APITiktok(object):
    def __init__(self):
        self.url_main = ''
        self.url_user_feed = self.url_main + 'user/posts'
        self.url_user_detail = self.url_main + 'user/info'
        self.url_user_following = self.url_main + 'user/following'
        self.url_user_follower = self.url_main + 'user/follower'
        self.url_trending_region = self.url_main + 'feed/list'
        self.url_search_keyword = self.url_main + 'feed/search'
        self.url_search_hashtag = self.url_main + 'challenge/search'
    
    def GetUserFeed(self, userID, cursor='0'):
        params = {
            "unique_id":userID,
            "count":"30",
            "cursor":cursor
        }
        try:
            reponsive = requests.get(url=self.url_user_feed, params=params)
            return reponsive.json()
        except requests.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return error
        
    def DownWithoutWatermark(self, id, hd='1'): # 6996665911927262466 | https://vt.tiktok.com/XXXXXX | https://www.tiktok.com/@umay_874/video/6996665911927262466
        params = {
            "url":id,
            "hd":hd
        }
        try:
            reponsive = requests.get(url=self.url_main, params=params)
            return reponsive.json()
        except requests.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return error
        
# a = APITiktok()
# b = a.DownWithoutWatermark(id="7239703940600794374")
# print(b)
