try:
    import ujson as json
except:
    import json
import os
import dp
import conf

stat = None
def SetStat(x):
    global stat
    stat = x

def dpsolve(user, shorttext, head=True):
    global stat
    if head:
        shorttext = '-' + shorttext
    res = dp.Solve(user, shorttext, stat, best=1)[0]
    if head:
        res = res[1:]
    return res

lastuser = None
userhitlist = None
def GetUserHitList(user):
    global lastuser, userhitlist
    if lastuser != user:
        lastuser = user
        userhitlist = json.load(open(os.path.join(conf.USERGRAM_DIR, user+'.json'), 'r'))
    return userhitlist

def Predict(user, shortentities):
    return MatchWithHit(user, dp.GetTextFromShortenedEntities(shortentities), GetUserHitList(user))

def MatchWithHit(user, shorttext, userhits, minhit=3, maxhit=6):
    def greedy(left, right, maximum=1):
        if right - left < 3:
            return [[]]
        candidates = []
        for l in range(maxhit, minhit-1, -1):
            if len(candidates) >= maximum:
                break
            localcandidates = []
            for i in range(left, right - l + 1):
                substr = shorttext[i:i+l]
                if substr in userhits[l - minhit]:
                    localcandidates.append((userhits[l - minhit][substr][1], (i, i + l)))
            if localcandidates:
                localcandidates = zip(*sorted(localcandidates))[1]
                candidates += localcandidates[len(candidates) - maximum:]
        res =  [greedy(left, candidate[0])[0] + [candidate]+ greedy(candidate[1], right)[0] for candidate in candidates]
        if len(res) == 0:
            return [[]]
        return res

    def complete(matched):
        n = len(shorttext)
        text = [None] * n
        for l, r in matched:
            text[l:r] = userhits[r - l - minhit][shorttext[l:r]][0]
        notcompleted = []
        i = 0
        while i < n:
            j = i
            while j < n and text[j] is None:
                j += 1
            notcompleted.append((i, j))
            i = j
            while i < n and text[i] is not None:
                i += 1
        for l, r in notcompleted:
            text[l:r] = dpsolve(user, shorttext[l:r], l==0)
        return text

    if isinstance(shorttext, list):
        shorttext = ''.join(shorttext)
    res = greedy(0, len(shorttext), 3)
    res = list(set(map(tuple, res)))
    # print res
    return map(complete, res) + ([dpsolve(user, shorttext)] if len(res) < 3 else [])


if __name__ == '__main__':
    print 'test MatchWithHit'
    SetStat(dp.Stat())
    shorttext = 'xbbbbxxcccaaaaaaddd'
    userhitlist = [{'ddd':(('D', 'D', 'D'), 1, 1), 'ccc':(('C', 'C', 'C'), 1, 1)}, {'bbbb':(('B', 'B', 'B', 'B'), 1, 1)}, {}, {'aaaaaa':(('A', 'A', 'A', 'A', 'A', 'A'), 1, 1)}]
    print MatchWithHit('ecvla', shorttext, userhitlist)

