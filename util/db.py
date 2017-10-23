import pymongo

from config import *

class MongoClient(object):
    def __init__(self):
        self._client = pymongo.MongoClient(MONGO_URL)

    def get_rooms(self):
        db = self._client[MONGO_DB]
        for room in db[MONGO_TABLE].find(): # 去掉limit
            yield {
                'r_id' : room['r_id'],
                'r_name' : room['r_name']
            }
    def set_label(self, **kwargs):
        self._client[MONGO_DB][MONGO_TABLE].\
           update(kwargs['query'], kwargs['data'], upsert=False)

    def save(self, msg):
        try:
            self._client[MONGO_DB][MONGO_HERO_NAME].insert(msg)
        except Exception as e:
            print("e: ", e)
    def get_hero_name_list(self):
        for hero_name in self._client[MONGO_DB][MONGO_HERO_NAME].find():
            for name in hero_name['hero_name_list']:
                yield name


