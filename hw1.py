# Nate Close: closen@seas.upenn.edu
# Jason Mow: jmow@seas.upenn.edu

# Import the corpus reader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from math import sqrt

# lists all sub-directories from this directory
# Functional, but does not work on empty directories!
def get_sub_directories(directory):
    files = PlaintextCorpusReader(directory, ".*")
    dirs = list()
    for f in files.fileids():
        if "/" in f:
            if (f[:f.index("/")] not in dirs):
                dirs.append(f[:f.index("/")])
    return dirs

# gets all files in this directory and its sub-directories
def get_all_files(directory):
    files = PlaintextCorpusReader(directory, '.*')
    return files.fileids() 

# returns a list of all sentences in that file
def load_file_sentences(filepath):
    file1 = open(filepath)
    sent = file1.read()
    sent = sent.lower()
    return sent_tokenize(sent)

# load all sentences in files within this drectory
# should return list of sentences
def load_collection_sentences(directory):
    files = get_all_files(directory)
    li = list()
    for f in files:
        sents = load_file_sentences(directory + "/" + f)
        li.extend(sents)
    return li

# returns a list of all tokens in a file
def load_file_tokens(filepath):
    file1 = open(filepath)
    text = file1.read()
    text = text.lower()
    return word_tokenize(text)

# load all tokens in files within this directory
# should return list of tokens
def load_collection_tokens(directory):
    files = get_all_files(directory)
    li = list()
    for f in files:
        tokens = load_file_tokens(directory + "/" + f)
        li.extend(tokens)
    return li

# SECTION 2

# load most frequent n words associated with a file or collection
def get_top_words(path, n):
    files = get_all_files(path) # returns [] if path is a file
    fdist = FreqDist()
    if(len(files) == 0):
        for word in load_file_tokens(path):
            fdist.inc(word)
    else:
        for word in load_collection_tokens(path):
            fdist.inc(word)  
    li = fdist.keys()
    return li[:n]

def get_top_words_with_stoplist(path, n):
    # read in stoplist file
    stoplistfile = open('/home1/c/cis530/hw1/stoplist.txt')
    stoplist = [line.strip() for line in stoplistfile]

    files = get_all_files(path) # returns [] if path is a file
    fdist = FreqDist()
    if(len(files) == 0):
        for word in load_file_tokens(path):
            if(word not in stoplist):
                fdist.inc(word)
    else:
        for word in load_collection_tokens(path):
            if(word not in stoplist):
                fdist.inc(word)  
    li = fdist.keys()
    return li[:n]

def load_topic_words(topic_file):
    dict1 = {}
    file1 = open(topic_file)
    for line in file1:
        x = line.strip().split(' ')
        dict1[x[0]] = float(x[1])
    return dict1

def get_top_n_topic_words(topic_words_dict, n):
    li = list()
    for w in sorted(topic_words_dict, key=topic_words_dict.get, reverse=True):
        li.append(w)
    return li[:n]

def create_feature_space(inputlist):
    dict1 = {}
    index = 0
    for sent in inputlist:
        for word in sent.split(' '):
            if word not in dict1:
                dict1[word] = index
                index += 1
    return dict1

def vectorize(feature_space, string):
    tokens = word_tokenize(string)
    li = list()      
    for i in range(len(feature_space)):
        li.append(0)
    for word in tokens:
        if word in feature_space:
            li[feature_space[word]] = 1
    return li

def dice_similarity(x, y):
    sumMin, sumSum = 0
    for i in range(min(len(x), len(y))):
        sumMin += min(x[i], y[i])
        sumSum += x[i] + y[i]
    return 2 * sumMin / sumSum

def jaccard_similarity(x, y):
    sumMin = 0
    sumMax = 0
    n = min(len(x), len(y))
    for i in range(n):
        sumMin += min(x[i], y[i])
        sumMax += max(x[i], y[i])
    return sumMin/sumMax

def cosine_similarity(x, y):
    prodCross = 0
    xSquare = 0
    ySquare = 0
    for i in min(len(x), len(y)):
        prodCross += x[i] * y[i]
        xSquare += x[i] * x[i]
        ySquare += y[i] * y[i]
    return prodCross / (sqrt(xSquare) * sqrt(ySquare))

