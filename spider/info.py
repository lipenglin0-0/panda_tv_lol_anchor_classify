import time
from datetime import datetime

import pymongo
import requests

from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def searchId(url, payload):
    r = requests.get(url=url, params=payload)
    '''
    json:
    loads: 将json转成python对象，反序列化
    dumps: 反之
    load/dump：处理文件
    '''
    return r.json()

def save_to_mongo(res):
    try:
        if not db[MONGO_TABLE].find({"r_id": res["r_id"]}).limit(1).count() > 0: # 根据"r_id"去重
            db[MONGO_TABLE].insert(res)
    except Exception:
        print("error: ", res)

def main():
    url = "http://www.panda.tv/ajax_sort"
    payload = {
        "pageno" : "1",
        "pagenum" : "120",
        "classification" : "lol"
    }
    # 注意 i
    i = 1
    while True:
        payload["pageno"] = i
        data = searchId(url=url, payload=payload)
        items = data["data"]["items"]
        # 判断items 是否为空
        if items:
            for item in items:
                room = {
                    "r_id": item["id"],
                    "r_name": item["name"],
                    "r_classification": item["classification"],
                    "u_name": item["userinfo"]["nickName"],
                    "u_avatar_url": item["userinfo"]["avatar"],
                    "time" : datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                }
                save_to_mongo(room)

            print ("已保存第", i, " 页房间信息！")
        else:
            print("一共", i-1, " 页！")
            break
        i += 1

if __name__ == '__main__':
    while True:
        main()
        print("睡眠中……")
        time.sleep(60*1)


