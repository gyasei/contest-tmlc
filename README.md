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
