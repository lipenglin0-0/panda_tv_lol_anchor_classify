import requests
from pyquery import PyQuery as pq

from config import MY_DICT
from util.db import MongoClient

db = MongoClient()

def get_label(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    }
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8' # 通过r.encoding设置页面编码
    doc = pq(r.text)
    table = doc.find('body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-child(154) > tr').items()
    id = 0
    for tr in table:
        if tr.find('td'): # 去掉th
            '''
            “凤凰传奇”是同时发布的，序号在一起，需要单独修改一下，mydict 也修改一下
            db.getCollection('hero').update(
                // query 
                {
                    "hero_name" : "洛"
                },
                
                // update 
                { '$set' : {'hero_name' : '幻翎', 'hero_name_list' : ['幻翎', '洛'], "join_time" : "2017年4月18日"}
                },
                
                // options 
                {
                    "multi" : false,  // update only one document 
                    "upsert" : false  // insert a new document, if no existing document match the query 
                }
            );
            '''
            id += 1
            hero_name = tr.find('td:nth-child(2)').text().strip()
            hero_name_list = []
            hero_name_list.append(tr.find('td:nth-child(2)').text().strip())
            hero_name_list.append(tr.find('td:nth-child(3)').text().strip())
            join_time = tr.find('td:nth-child(6)').text().strip()
            msg = {
                'id' : id,
                'hero_name' : hero_name,
                'hero_name_list' : hero_name_list,
                'join_time' : join_time
            }
            print(msg)
            db.save(msg)

def make_mydict():
    with open(MY_DICT, mode='w', encoding='utf-8') as f:
        for name in db.get_hero_name_list():
            print(name, file=f) # 直接换行

if __name__ == '__main__':
    get_label('https://baike.baidu.com/item/英雄联盟/4615671#4')
    make_mydict() # 创建词典
    print('ok...')

