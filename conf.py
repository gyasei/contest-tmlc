ORIGIN_TRAIN_DIR = '../data/original-trainset/'
DIR = '../data/userdata/'
USERGRAM_DIR = '../data/usergram/'

TRAIN_RATIO = 0.9
VOCAB_BG_MIN_NUMBER = 100    # Only consider those vocab whose number >= VOCAB_MIN_NUMBER
VOCAB_USER_MIN_NUMBER = 5
MINN=3
MAXN=6
BG1_FILE = DIR+'bg-1grams.json'
BG2_FILE = DIR+'bg-2grams.json'
USER1_FILE = DIR+'user-1grams.json'
USER2_FILE = DIR+'user-2grams.json'
USERLIST = DIR+'users.json'
