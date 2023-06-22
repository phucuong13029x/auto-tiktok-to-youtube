from app.wkn_config import *
from app.wkn_control import printDefault, checkLicense, wait_time, writeJson, readJson
from app.wkn_tiktok import APITiktok
from app.wkn_youtube import get_authenticated_service, initialize_upload
from app.wkn_facebook import Facebook
from urllib.request import urlretrieve, urlopen
from datetime import datetime, time, timedelta
import sys
import time as times

def loadInfo(id, cur):
    res = {}
    conn = APITiktok()
    data = conn.GetUserFeed(userID=id, cursor=cur)
    for i in data['data']['videos']:
        res[int(i['create_time'])] = {"video_id":i['video_id']}
    index = {"hasMore":data['data']['hasMore'], "cursor":data['data']['cursor']}
    return index, res

def arrangeList(args):
    listKey = sorted(args.keys())
    dictKetQua = {}
    for key in listKey:
        dictKetQua[key] = args[key]
    return dictKetQua

if __name__ == '__main__':
    try:
        # CONVERT DAY & TIME
        if conf_scheduler_day and conf_scheduler_day != "":
            convert_day = []
            for i in conf_scheduler_day:
                convert_day.append(int(i))
        if conf_scheduler_time and conf_scheduler_time != "":
            convert_time = []
            for i in conf_scheduler_time:
                convert_time.append(datetime.strptime(i, '%H:%M:%S').time())
        # CHECK LICENSE
        printDefault("0. LOAD CONFIG")
        print("- Check License")
        # license_check = checkLicense(conf_access_token, conf_license)
        license_check = 1
        if license_check == 1:
            # AYTHEN YOUTUBE API
            if conf_youtube == "true" and os.path.isfile(conf_youtube_client_secret) is True:
                print("- Authen Youtube API V3")
                youtube = get_authenticated_service(CLIENT_SECRETS=conf_youtube_client_secret)
                sys.stdout.write('\r')
            # LOAD VIDEO
            allData = {}
            cursor = "0"
            try:
                if conf_tiktok_video == "all":
                    printDefault("1. PLEASE WAIT LOAD ALL VIDEO TO CHANNEL")
                    while True:
                        r, v = loadInfo(id=conf_tiktok_userid, cur=cursor)
                        allData.update(v)
                        if r['hasMore'] is not True:
                            break
                        else:
                            cursor = r['cursor']
                        wait_time(number=11, text=f"- Load more ({len(allData)})... ")
                    print("\n")
                elif conf_tiktok_video == "new":
                    printDefault("1. PLEASE WAIT LOAD NEW VIDEO TO CHANNEL")
                    r, v = loadInfo(id=conf_tiktok_userid, cur=cursor)
                    allData.update(v)
            except Exception as e:
                print(e)
            tiktok_path_channel = basedir_data + os.sep + conf_tiktok_userid
            os.makedirs(tiktok_path_channel, exist_ok=True)
            # CHECK DATA INFO
            if os.path.isfile(tiktok_path_channel + os.sep + 'info.json') is True:
                loadData = readJson(tiktok_path_channel + os.sep + 'info.json')
                for i in loadData:
                    for j in allData:
                        if i == j:
                            allData.pop(j)
                            break
                for i in allData:
                    loadData.update(i)
                print("- Save info to json file")
                writeJson(tiktok_path_channel, loadData)
            else:
                print("- Save info to json file")
                writeJson(tiktok_path_channel, allData)
            conf_tiktok_video = "new"
            allData = arrangeList(args=allData)
            # IN PROCESS
            convert_time_one = convert_time
            if allData and allData != '':
                for i in allData:
                    print(i, conf_tiktok_startin, int(i), int(conf_tiktok_startin))
                    if int(allData[i]['video_id']) > int(conf_tiktok_startin):
                        tiktok_path_download = tiktok_path_channel + os.sep + allData[i]['video_id'] + '.mp4'
                        try:
                            # Download video
                            print("- Start download video...")
                            conn = APITiktok()
                            create_download = conn.DownWithoutWatermark(id=allData[i]['video_id'])['data']
                            urlretrieve(create_download['hdplay'], tiktok_path_download)
                            print(f"- Download video: {tiktok_path_download}")
                            if conf_youtube == "true" or conf_facebook == "true":
                                stop_upload = 0
                                date_now = datetime.now().day
                                while True:
                                    if datetime.now().weekday() in convert_day:
                                        if convert_time_one and convert_time_one != '':
                                            for i in convert_time_one:
                                                now = datetime.now().time()
                                                time_5_minute = time(i.hour, i.minute + 5, i.second)
                                                if now > i and now < time_5_minute:
                                                    if conf_facebook == "true":
                                                        print("\n- Upload video Facebook...")
                                                        # Upload video facebook
                                                        connectfb = Facebook(access_token=conf_facebook_access_token, pageid=conf_facebook_pageid)
                                                        title = create_download['title']
                                                        if title.find('#') != -1:
                                                            title_convert = title[:int(title.find('#'))]
                                                            if title_convert != '':
                                                                title = title_convert
                                                            else:
                                                                title = conf_youtube_title + f' #{int(times.time())}'
                                                        else:
                                                            title = conf_youtube_title + f' #{int(times.time())}'
                                                        uploadfb = connectfb.upload(video_path=tiktok_path_download, title=title, description=create_download['title'])
                                                        if uploadfb is True:
                                                            print("- Upload facebook success.")
                                                            stop_upload = 1
                                                            convert_time_one.remove(i)
                                                        elif uploadfb is False:
                                                            print("- Upload facebook fail")
                                                        else:
                                                            print(f"- {uploadfb}")
                                                    if conf_youtube == "true":
                                                        # Upload video Youtube
                                                        print("- Upload video Youtube...")
                                                        title = create_download['title']
                                                        description = create_download['title']
                                                        keywords = create_download['title'].replace("#", ",")
                                                        category = str(conf_youtube_category)
                                                        if title.find('#') != -1:
                                                            title_convert = title[:int(title.find('#'))]
                                                            keywords = title.replace("#", ",")
                                                            if title_convert != '':
                                                                title = title_convert
                                                            else:
                                                                title = conf_youtube_title + f' #{int(times.time())}'
                                                        else:
                                                            title = conf_youtube_title + f' #{int(times.time())}'

                                                        if conf_youtube_description != '':
                                                            description = conf_youtube_description
                                                        # if conf_youtube_keywords != '':
                                                        #     keywords = conf_youtube_keywords
                                                        args = {"file": tiktok_path_download, "title": title, "description": description, "category": conf_youtube_category, "keywords": keywords, "privacyStatus": conf_youtube_privacyStatus}
                                                        initialize_upload(youtube, args)
                                                        stop_upload = 1
                                                        try:
                                                            convert_time_one.remove(i)
                                                        except:
                                                            pass
                                                elif now > time_5_minute:
                                                    convert_time_one.remove(i)
                                            if stop_upload == 1:
                                                break
                                            if convert_time_one:
                                                sys.stdout.write('\r')
                                                sys.stdout.write("- Next time: %-8s" % convert_time_one[0])
                                        else:
                                            if date_now < datetime.now().day:
                                                print("\n- Reset schedule on day.")
                                                for i in conf_scheduler_time:
                                                    convert_time_one.append(datetime.strptime(i, '%H:%M:%S').time())
                                                print(convert_time_one, convert_time)
                                                date_now = datetime.now().day
                                            else:
                                                wait_time(number=240, text="- Posting time has expired. ")
                                    else:
                                        wait_time(number=86400, text="- No posting schedule today. ")
                        except Exception as e:
                            pass
            allData = []
        else:
            printDefault(f"ERROR: YOUR IS LICENSE INVALID")

    except Exception as e:
        print(e)
    exit("PRESS ENTER TO EXIT: ")
