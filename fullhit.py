import os
import conf
import util
import math
from tqdm import tqdm
from collections import defaultdict
try:
    import ujson as json
except:
    import json

stat = None
def SetStat(x):
    global stat
    stat = x

def getKeyfromEntities(entities):
    return ''.join(x[0] for x in entities)

def build():
    D = {}
    users = json.load(file(conf.USERLIST))
    for user in tqdm(users):
        trainfile = os.path.join(conf.DIR, user+'-train.json')
        tweets = json.load(file(trainfile))
        for tweet in tweets:
            text = list(map(util.process_token, tweet['entitiesFull']))
            if len(text) < 3:
                continue
            key = getKeyfromEntities(text)
            if key not in D:
                D[key] = defaultdict(set)
            D[key][user].add(tuple(text))
    return D

def textProbability(user, text):
    global stat
    p = 0.0
    for t in text:
        p += math.log(stat.user_n1gram[user].get(t, 0) + 1.0)
    return p

def predict(D, user, entitiesShortened, best=3):
    entities = map(util.process_token, entitiesShortened)
    key = getKeyfromEntities(entities)
    if key not in D:
        return False, []
    else:
        texts = []
        if user in D[key]:
            for text in D[key][user]:
                p = textProbability(user, text)
                texts.append((text, p))
        else:
            for _ in D[key]:
                for text in D[key][_]:
                    p = textProbability(user, text)
                    texts.append((text, p))
        texts = sorted(texts, key=lambda(x,y): -y) if len(texts) > 3 else texts
        return True, [util.Recover(text[0], entitiesShortened) for text in texts[:best]]

if __name__ == '__main__':
    print "test build..."
    D = build()

