import pyrebase
from requests import HTTPError
import json


firebaseConfig = {
    "apiKey": "AIzaSyBttYR3fweoJKqnbtdRlcO2AwcbtzktSOs",
    "authDomain": "dbstoreapi.firebaseapp.com",
    "databaseURL": "https://dbstoreapi-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "dbstoreapi",
    "storageBucket": "dbstoreapi.appspot.com",
    "messagingSenderId": "451333344216",
    "appId": "1:451333344216:web:7cbab822c07a749d7540ad",
    "measurementId": "G-PCNVLP8MYT"
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
        