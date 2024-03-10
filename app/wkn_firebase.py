import pyrebase
from requests import HTTPError
import json


firebaseConfig = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
}
firebase_Connect = pyrebase.initialize_app(firebaseConfig)
firebase_Database = firebase_Connect.database()

class DatabaseFB(object):
    def __init__(self):
        self.firebase_Database = firebase_Connect.database()

    def getDB(self, parent, child=None):
        try:
            if child is None:
                results = self.firebase_Database.child(parent).get()
            else:
                results = self.firebase_Database.child(parent).child(child).get()
            return results.val()
        except HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return error
        
