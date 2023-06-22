import os
from sys import stdout
import time
import json
from urllib.request import urlopen
import re as r
from app.wkn_firebase import DatabaseFB


def readFile(path):
    if os.path.isfile(path) is True:
        list_out = []
        with open(path, "r", encoding="utf8") as f:
            lines = f.readlines()
            f.close()
        for i in lines:
            list_out.append(i.replace("\n", ""))
        return list_out
    return False

def printDefault(strs):
    print("="*50)
    print(strs)

def wait_time(number, text=""):
    for i in range(number):
        stdout.write('\r')
        if text != "":
            stdout.write(text)
        else:
            stdout.write('- ')
        stdout.write("Please wait after: %-4s second" % (number - i))
        time.sleep(1)

# GET IP PUBLIC
def getIP():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

def checkLicense(userid, key):
    data = DatabaseFB().getDB(parent='users', child=userid)
    data = json.loads(json.dumps(data))
    license_check = ""
    if data['license'][0]['key'] == key and data['ip'] == getIP() and data['license'][0]['expires'] >= time.time():
        license_check = 1
    return license_check

def writeJson(path, data):
    with open(path + os.sep + "info.json", "w", encoding="utf8") as f:
        json.dump(data, f)
        f.close()

def readJson(path):
    f = open (path, "r", encoding="utf8")
    data = json.loads(f.read())
    return data
