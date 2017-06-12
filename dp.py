from collections import defaultdict
import math
import time
import os
from tqdm import tqdm
try:
    import ujson as json
except:
    import json
import conf
import util

class Stat:
    def __init__(self, bg_n1file=conf.BG1_FILE, bg_n2file=conf.BG2_FILE, user_n1file=conf.USER1_FILE, user_n2file=conf.USER2_FILE):
        print 'Read json files...'
        self.bg_n1gram = json.load(file(bg_n1file))
        self.bg_n2gram = json.load(file(bg_n2file))
        self.user_n1gram = json.load(file(user_n1file))
        self.user_n2gram = json.load(file(user_n2file))
        print 'Load grams...'
        tic = time.time()
        self.bg_vocab = defaultdict(lambda : defaultdict(int))
        self.user_vocab = defaultdict(lambda : defaultdict(lambda: defaultdict(int)))
        for i, j in self.bg_n1gram.iteritems():
            self.bg_vocab[i[0]][i] = j
        for user in self.user_n1gram:
            for i, j in self.user_n1gram[user].iteritems():
                self.user_vocab[user][i[0]][i] = j

        self.bg_probs = defaultdict(lambda : defaultdict(list))
        self.bg_count = defaultdict(lambda : defaultdict(int))
        self.user_probs = { user:defaultdict(lambda : defaultdict(list)) for user in self.user_n1gram }
        self.user_count = { user: defaultdict(lambda : defaultdict(int)) for user in self.user_n1gram }

        for a, d in self.bg_n2gram.iteritems():
            for b, k in d.iteritems():
                self.bg_probs[a][b[0]].append((b, k))
                self.bg_count[a][b[0]] += k
        for user in self.user_n1gram:
            for a, d in self.user_n2gram[user].iteritems():
                for b, k in d.iteritems():
                    self.user_probs[user][a][b[0]].append((b, k))
                    self.user_count[user][a][b[0]] += k
        print 'loaded. Takes %f seconds.' % (time.time() - tic)

    # if c in self.user_vocab[user], then return user's vocabs. Otherwise, return background's.
    def GetVocab(self, user, c):
        return self.user_vocab[user].get(c, self.bg_vocab.get(c, {})).keys()

    def GetDistribution(self, user, c):
        if c == '-':
            return {'-':1}
        else:
            d = self.user_vocab[user].get(c, self.bg_vocab.get(c, {}))
            return d

    # if [w][c] in self.user_probs[user], then return user's probs and count. Otherwise, return background's.
    def GetProbs(self, user, w, c):
        return self.user_probs[user].get(w, {}).get(c, self.bg_probs.get(w, {}).get(c, [])), \
                self.user_count[user].get(w, {}).get(c, self.bg_count.get(w, {}).get(c, 0))


def Solve(user, text, stat, best=3):
  v = stat.GetDistribution(user, text[0])
  cur = [(math.log(j), [i]) for i, j in v.iteritems()]

  for t in text[1:]:
    next = {v : (-float('inf'), None) for v in stat.GetVocab(user, t)}
    m = len(next)
    for p, l in cur:
      d, n = stat.GetProbs(user, l[-1], t)
      for w, cnt in d:
        if w not in next:
          continue
        next_p = p + math.log(cnt + 1) - math.log(n + m)
        if next[w][0] < next_p:
          next[w] = (next_p, l + [w])

      min_p = p - math.log(n + m)
      for w, (p, _) in next.iteritems():
        if p < min_p:
          next[w] = (min_p, l + [w])
      cur = next.values()

  return zip(*(sorted(cur)[-best:]))[1]


def GetTextFromShortenedEntities(entities):
  return map(util.process_token, entities)


def Predict(user, entities, stat, best=3):
  texts = Solve(user, GetTextFromShortenedEntities(entities), stat, best)
  return [util.Recover(text, entities) for text in texts]


