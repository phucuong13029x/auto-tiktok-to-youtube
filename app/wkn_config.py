import os
from configparser import ConfigParser


# DEFAULT
info_title = "Tiktok Auto Tool"
info_version = "1.0"
info_author = "phucuongds.com"
basedir = os.getcwd()


# FOLDER & FILE
os.makedirs(basedir + os.sep + 'setting', exist_ok=True)
os.makedirs(basedir + os.sep + 'data', exist_ok=True)
basedir_extensions = basedir + os.sep + 'setting'
basedir_data = basedir + os.sep + 'data'
file_link = basedir_extensions + os.sep + 'link.txt'
file_conf = basedir_extensions + os.sep + 'config.ini'


# LOAD CONFIG USER
conf = ConfigParser()
conf.read(file_conf, encoding = "utf8")

## License
conf_access_token = conf.get("LICENSE", "access_token")
conf_license = conf.get("LICENSE", "license")

## Tiktok
conf_tiktok_userid = conf.get("TIKTOK", "userid")
conf_tiktok_video = conf.get("TIKTOK", "video")
conf_tiktok_startin = int(conf.get("TIKTOK", "startIn"))

## Youtube
conf_youtube = conf.get("YOUTUBE", "value")
conf_youtube_title = conf.get("YOUTUBE", "title")
conf_youtube_description = conf.get("YOUTUBE", "description")
conf_youtube_category = conf.get("YOUTUBE", "category")
conf_youtube_keywords = conf.get("YOUTUBE", "keywords")
conf_youtube_privacyStatus = conf.get("YOUTUBE", "privacyStatus")
conf_youtube_client_secret = basedir_extensions + os.sep + 'client_secret.json'

## Facebook
conf_facebook = conf.get("FACEBOOK", "value")
conf_facebook_access_token = conf.get("FACEBOOK", "access_token")
conf_facebook_pageid = conf.get("FACEBOOK", "pageid")

## Scheduler
conf_scheduler_day = conf.get("SCHEDULER", "day").replace(" ","").split(",")
conf_scheduler_time = conf.get("SCHEDULER", "time").replace(" ","").split(",")
