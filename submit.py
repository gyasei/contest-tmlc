import requests
import sys
import json
from IPython import embed
import time
auth=('akovskiboy@gmail.com', 'e19bd2f5234ab55170a1b0bcdb0aee02')

def submitone(url, tweetid, predictions):
    resp = requests.post(url, json={'id':tweetid, 'predictions':predictions})
    print resp, resp.text
    return resp

def submit(filename):
    d = json.load(open(filename, 'r'))
    posturl='http://%s:%s@challenges.tmlc1.unpossib.ly/api/submissions'%auth
    ids = d.keys()
    #md = {}
    #with open('./missed.txt', 'r') as f:
    #    for l in f.readlines():
    #        l = l.strip()
    #        md[l] = d[l]
    #d = md
    #for tid in ids[:500]:
    #    print submitone(posturl, tid, d[tid]).text
    #    time.sleep(1)
    #d = {k:d[k] for k in ids[500:]}
    #embed() # pre-check
    resp = requests.post(posturl, json=d)
    #embed() # post-check
    print resp, resp.text
    print 'total words: ', sum(len(x[0]) for x in d.values())

if __name__ == '__main__':
    submit(sys.argv[1])


