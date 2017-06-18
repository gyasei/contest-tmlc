# Requirements

- python 2.7.6
- python package tqdm ( which can be easily installed by `pip install tqdm` )
- at least 20GB memory CPU

# Usage

### Step 1: prepare dataset

Put all dataset into one folder.

### Step 2: configure and  preprocess

Change **conf.py** and make sure that 
- `ORIGIN_TRAIN_DIR` refers to the dataset folder
- `DIR` and `USERGRAM_DIR` are created

Then just run **preprocess.py** to obtain statistic training results such as 1-grams and 2-grams.

### Step 3: predict

```
python main.py --input path/to/your/input/file --output path/to/your/output/file
```

The format of input file and output file is totally the same as that of the scoring phase's.

# Approach

### Process Data
Since there are difference type of tokens in tweets, we treat all token as word. For special token like url or usermetion, they are transformed to different ascii code like ```@``` or ```#```. In this way, we can handle all tokens as words, no need to check what's special token or not. This makes things easier at training and predicting stage. For numbers, we also convert all of them to `!`, when we predict, just predict the digit.

We also lower all word for training so that when we predict, we only 

For example, a tweet like ```[UserMention] Hi, There are interesting 2 links [Url], [Url]```, then it will transformed to ```@ hi there are interesting ! links # #```. They are all words with no diffence now!

You can refer to ```utils.py``` for more details.

### DP method
We start with a naive method based on dynamic programming and 2-gram frequency.  
The idea is simple: go through the letters and generate word one by one, which word to choose is based last word we found. This yields a standard dynamic programming algorithm: maximize ```Q(n,X_n)=P(X_1)*P(X_2|X_1)*P(X_3|X_2)*...*P(X_n|X_n-1)))```, where ```X_i```is the i-th word given first letter and ```P(X_i|X_i-1)```can be obtained by ```2gramfreq(X_i,X_i-1)/2gramfreq(X_i, *)```.  

In this method, we can iterate through a sequence and  maintain probablity of first n words which ending with a specific word as ```Q(n, X_n)```, then update ```Q(n+1, X_n+1)``` accordingly. See ```dp.Solver``` for how is it implemented.  

This model looks ideal. However, it performs badly (14% accuracy on validation dataset) because it only considers two adjenct words rather than the sentence as the whole. It produces sentences which don't make sense at all. So later we only use it as fallback when other methods don't work :)

### Hit method

After failing on dp method, we started lookint into the data itself. Surprisingly, we found that sometimes many tweets from one user are very similar! This gave us a hint that we should try to match user's tweets as much as possbile. 

At the first, we stored all leading letter squences of training data. On test phase, we just look up whether there is a same squence in training data. If true, just output result as the found sentence. There are >25% duplicated tweets in traing data, which means you can get 25% of fullscore by just looking for duplicated tweets! We call this part as ```fullhit```, you can refer to ```fullhit.py``` for details.

We are not satisfied with this. After this it's very natural to think about matching part of a squence. So this time, we stored all subsequence of tweets (for squence ```X_1...X_n```, subsequence is all ```X_i...X_j``` where ```1<=i<=j<=n```) with length between 3 and 6 (this number is just some randomly chose number, it can be 7,8 or even more, but watch out for memory space!). We just keep the most frequent subsequence if multiple different sequences have the same leading letters. On predict phase, try to match a subsequence as long as possbile, if matched, split the unmatched parts, do the same thing recursively. We also need to consider cases when there are parts of sentence not matched, then just treat them single sentence and predict them using DP method! You can refer to ```hitmethod.Predict``` for implementation. 

