import os
import conf
import util
from tqdm import tqdm
try:
    import ujson as json
except:
    import json
from collections import defaultdict

def readdir(dir, userdata):
    print 'read', dir
    for f in tqdm(os.listdir(dir)):
        for data in json.load(open(os.path.join(dir, f))):
            user = data['user']
            data = { i: data[i] for i in ['id', 'entitiesFull', 'entitiesShortened', 'quotedText'] }
            if user not in userdata:
                userdata[user] = []
            userdata[user].append(data)

def collectTrain():
    userdata = {}
    for dir in [conf.ORIGIN_TRAIN_DIR]:
        readdir(dir, userdata)
    print 'write ...'
    json.dump(userdata.keys(), file(conf.USERLIST, 'w'))
    for user in tqdm(userdata):
        json.dump( userdata[user], file(os.path.join(conf.DIR, user+'-train.json'), 'w'))
    print 'Finish'
    return userdata

def fucklambda():
    return defaultdict(int)

def trainUser1and2Grams(userdata):
    data_train = userdata
    bg_1gram, bg_2gram = defaultdict(int), defaultdict(fucklambda) # background
    user_1gram = { user: defaultdict(int) for user in data_train }
    user_2gram = { user: defaultdict(fucklambda) for user in data_train }
    print 'Count 1grams...'
    for user, tweets in tqdm(data_train.items()):
        for tweet in tweets:
            text = list(map(util.process_token, tweet['entitiesFull']))
            for word in text:
                bg_1gram[word] += 1
                user_1gram[user][word] += 1
    # background vocab excludes those numbers < VOCAB_BG_MIN_NUMBER
    bg_1gram = { k:v for k, v in bg_1gram.items() if v >= conf.VOCAB_BG_MIN_NUMBER }
    # user vocab excludes those numbers < VOCAB_USER_MIN_NUMBER
    for user in data_train:
        user_1gram[user] = { k:v for k, v in user_1gram[user].items() if v >= conf.VOCAB_USER_MIN_NUMBER }
    print 'Count 2grams...'
    for user, tweets in tqdm(data_train.items()):
        for tweet in tweets:
            text = ['-'] + list(map(util.process_token, tweet['entitiesFull']))
            for word1, word2 in zip(text[:-1], text[1:]):
                if (word1 == '-' or word1 in bg_1gram) and word2 in bg_1gram:
                    bg_2gram[word1][word2] += 1
                if (word1 == '-' or word1 in user_1gram[user]) and word2 in user_1gram[user]:
                    user_2gram[user][word1][word2] += 1
    print 'write...'
    json.dump(bg_1gram, file(conf.BG1_FILE, 'w'))
    json.dump(bg_2gram, file(conf.BG2_FILE, 'w'))
    json.dump(user_1gram, file(conf.USER1_FILE, 'w'))
    json.dump(user_2gram, file(conf.USER2_FILE, 'w'))
    print 'Finish'

if __name__ == '__main__':
    userdata = collectTrain()
    trainUser1and2Grams(userdata)
