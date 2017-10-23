import jieba

from config import MY_DICT
from util.db import MongoClient

class Tokenizer(object):
    def __init__(self):
        self._db = MongoClient()
        # 载入自己的词库
        jieba.load_userdict(MY_DICT)

    def get_hero_list(self):
        hero_list = []
        with open(MY_DICT, mode='r', encoding='utf-8') as f:
            for hero in f:
                hero_list.append(hero.strip())
        return hero_list

    def participle(self):
        hero_list = self.get_hero_list()
        print('/'.join(hero_list))
        for room in self._db.get_rooms():
            # 分词 [默认精确]
            msg = jieba.lcut(room['r_name'])
            label_list = set([w for w in msg if w in hero_list]) # 去重复
            self._db.set_label(query={'r_id' : room['r_id']},
                               data={'$set' : {'r_label' : list(label_list)}})
            print(msg, label_list)

if __name__ == '__main__':
    # 标记
    tokenizer = Tokenizer()
    tokenizer.participle() # 分词