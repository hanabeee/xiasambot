
#                    Copyright (c) 2021 Zenqi.
#                 This project was created by Discord CLI
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pymongo import MongoClient


class SETTINGS:
    HOST        = "@pymongo_host"
    DATABASE    = "databse_name"
    STICKY_COLLECTION  = "create_collection_for_sticky"
    AFK_COLLECTION  = "create_collection_for_afg"
    
class Database:
    """
    Main class for handling database.
    """
    cluster: MongoClient = None
    def __init__(self):
        self.connect()
        self.db = self.cluster[SETTINGS.DATABASE]
        self.sticky_collection = self.db[SETTINGS.STICKY_COLLECTION]
        self.afk_collection = self.db[SETTINGS.AFK_COLLECTION]

    def connect(self):
        self.cluster = MongoClient(SETTINGS.HOST)
        
    def add_sticky_data(self, user: dict):
        return self.sticky_collection.insert_one(user)


    
