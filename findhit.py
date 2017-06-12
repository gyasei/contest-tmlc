try:
    import ujson as json
except:
    import json
from collections import defaultdict
import conf
import util
import os
import sys

def GetAllTweetsByUserSeparate():
    userlist = json.load(open(conf.USERLIST, 'r'))
    for user in userlist:
        tweets = json.load(open(os.path.join(conf.DIR, user+'-train.json')))
        yield user, [(map(util.process_token, t['entitiesFull']), ''.join(map(util.process_token, t['entitiesShortened'])) ) for t in tweets]

def GetMinFreqForNgramHit(n, user):
    if user is not None:
        return {3:5, 4:1, 5:1, 6:1, 7:1}[n]
    return 0

def ExtractHighFreqGrams(tweets, user=None):
    print user
    res = []
    for n in range(conf.MINN, conf.MAXN + 1):
        minfreq = GetMinFreqForNgramHit(n, user)
        d = defaultdict(lambda:defaultdict(int))
        for tweet, short in tweets:
            for j in range(0, len(tweet) - n):
                if True or user_n2grams[user][tweet[j]][tweet[j + 1]] >= minfreq:
                    key = short[j:j+n]
                    gram = tuple(tweet[j:j+n])
                    d[key][gram] += 1
        hits = dict()
        for shortkey, distribution in d.iteritems(): # get one candidate with maximum freq
            bestcandidate = max(distribution.iteritems(), key=lambda (x,y):-y)
            totalcnt = sum(distribution.values())
            if bestcandidate[1] >= minfreq and bestcandidate[1] >= totalcnt * 0.3: # at least it should appear enough times to be a candidate
                #if bestcandidate[1] != totalcnt:
                    #print distribution
                    #sys.exit(0)
                hits[shortkey] = bestcandidate + (totalcnt,)
        res.append(hits)
    return res

if __name__ == '__main__':
    for user, tweets in GetAllTweetsByUserSeparate():
        highfreqs = ExtractHighFreqGrams(tweets, user)
        #from IPython import embed; embed()
        json.dump(highfreqs, open(os.path.join(conf.USERGRAM_DIR, user + '.json'), 'w'))

