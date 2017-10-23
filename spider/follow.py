import pymongo
import requests

from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
'''
删除：
db.getCollection('id_tb').remove({
    "_id" : ObjectId("58e77b94a9231916402a4d8a"),
    "u_follower" : 11869
})
更新（删除某个属性）：
db.getCollection('id_tb').update(
{"r_id" : "419546"},
{"$unset":{"u_follower" : 91669}}
)
====================================
db.getCollection('id_tb').update(
{"u_follower" : [ 
        "fans"
    ]},
{"$unset":{"u_follower" : [ 
        "fans"
    ]}},
    {multi:true}
)
判断属性是否存在：
db.getCollection('id_tb').find({'r_id':{'$exists':true}})
'''
def get_room_followinfo():
    # http://www.panda.tv/room_followinfo?roomid=10447
    for u in db[MONGO_TABLE].find({'u_follower':{'$exists':False}}): # 没有 u_follower 属性
        url = "http://www.panda.tv/room_followinfo"
        r_id = u["r_id"]
        payload = {"roomid" : r_id}
        r = requests.get(url=url, params=payload)

        query = {"r_id": r_id}

        r_data = r.json()["data"] #如果是data 为空，则返回 str {}
        if not isinstance(r_data, str):
            u_follower = r_data["fans"]
            data = {
                "$set": {"u_follower": u_follower}  # 添加属性
            }
            db[MONGO_TABLE].update(query, data, upsert=False) #未找到，不插入属性
            print(db[MONGO_TABLE].find(query)[0]["u_name"], "订阅人数：", u_follower)
        else:
            db[MONGO_TABLE].remove(query)
            print("直播间房倒屋塌，对不起了”王姨“，拉黑ing~")

if __name__ == '__main__':
    get_room_followinfo()
