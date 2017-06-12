import dp
import fullhit
import conf
import hitmethod
import util
try:
    import ujson as json
except:
    import json
from tqdm import tqdm
import argparse

print 'Prepare for dp...'
stat = dp.Stat()
print 'Prepare for fullhit...'
ExactMatchDict = fullhit.build()
fullhit.SetStat(stat)
hitmethod.SetStat(stat)

def predict(user, entitiesShortened, best=3):
    hit, output = fullhit.predict(ExactMatchDict, user, entitiesShortened)
    if hit:
        return output
    res = hitmethod.Predict(user, entitiesShortened)
    res = [util.Recover(i, entitiesShortened) for i in res]
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input = json.load(file(args.input))
    results = dict()
    for tweet in tqdm(input):
        tweetid = tweet['id']
        predictions = predict(tweet['user'], tweet['entitiesShortened'])
        results[tweetid] = predictions
    json.dump(results, file(args.output, 'w'), indent=4)

