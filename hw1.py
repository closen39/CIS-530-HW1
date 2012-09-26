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
    sumMin = 0.0
    sumSum = 0.0
    for i in range(min(len(x), len(y))):
        sumMin += min(x[i], y[i])
        sumSum += x[i] + y[i]
    return 2 * sumMin / sumSum

def jaccard_similarity(x, y):
    sumMin = 0.0
    sumMax = 0.0
    n = min(len(x), len(y))
    for i in range(n):
        sumMin += min(x[i], y[i])
        sumMax += max(x[i], y[i])
    return float(sumMin/sumMax)

def cosine_similarity(x, y):
    prodCross = 0.0
    xSquare = 0.0
    ySquare = 0.0
    for i in range(min(len(x), len(y))):
        prodCross += x[i] * y[i]
        xSquare += x[i] * x[i]
        ySquare += y[i] * y[i]
    if (xSquare == 0 or ySquare == 0):
        return 0.0
    return prodCross / (sqrt(xSquare) * sqrt(ySquare))

def get_doc_vector(D, W):
    v = list()
    for i in range(len(W)):
        if W[i] in D:
            v.append(1)
        else:
            v.append(0)
    return v

def get_doc_sim(dir):
    s1 = get_top_words(dir + '/Starbucks', 50)
    h1 = get_top_words(dir + '/H.J.Heinz', 50)
    w1 = list(set(s1) | set(h1))

    s2 = get_top_words_with_stoplist(dir + '/Starbucks', 50)
    h2 = get_top_words_with_stoplist(dir + '/H.J.Heinz', 50)
    w2 = list(set(s2) | set(h2))

    t1 = load_topic_words('Starbucks_small.ts')
    s3 = get_top_n_topic_words(t1, 50)
    t2 = load_topic_words('Heinz_small.ts')
    h3 = get_top_n_topic_words(t2, 50)
    w3 = list(set(s3) | set(h3))

    # make a list out of these three values
    return [get_score(dir, w1), get_score(dir, w2), get_score(dir, w3)]


def get_score(dir, w):
    files = get_all_files(dir)
    totalScore = 0.0
    totalDocs = 0.0
    for file1 in files:
        tokens = set(load_file_tokens(dir + "/" + file1))
        v = get_doc_vector(tokens, w)
        countS = 0.0
        countH = 0.0
        simS = 0.0
        simH = 0.0
        for file2 in files:
            f2_tokens = set(load_file_tokens(dir + "/" + file2))
            f2v = get_doc_vector(f2_tokens, w)
            if 'Starbucks' in file2:
                countS += 1
                simS += cosine_similarity(v, f2v)
            elif 'H.J.Heinz' in file2:
                countH += 1
                simH += cosine_similarity(v, f2v)
        # calculate score using simS, simH and counts# calculate score using simS, simH and counts
        scoreS = (1 / countS) * simS
        scoreH = (1 / countH) * simH
        if 'Starbucks' in file1:
            totalScore += scoreS - scoreH
        else:
            totalScore += scoreH - scoreS
        totalDocs += 1
    return totalScore / totalDocs

def get_word_contexts(word, path):
    tokens = load_collection_tokens(path)
    context = set()

    while word in tokens:
        index = tokens.index(word)
        if index > 0:
            context.add(tokens[index-1])
        if index < len(tokens) - 1:
            context.add(tokens[index+1])
        tokens.remove(word)

    return list(context)

def get_common_contexts(word1, word2, path):
    l1 = get_word_contexts(word1, path)
    l2 = get_word_contexts(word2, path)

    return list(set(l1) & set(l2))

def compare_word_sim(path):
    tw = load_topic_words('Starbucks_small.ts')
    top_words = get_top_n_topic_words(tw, 10)
    contexts = list()

    for word in top_words:
        con = get_word_contexts(word, path)
        contexts.extend(con)

    fs = create_feature_space(contexts)
    context_vectors = list()
    for context in contexts:
        context_vectors.append(vectorize(fs, context))

    ret = list()
    for vector1 in context_vectors:
        temp = list()
        for vector2 in context_vectors:
            temp.append(cosine_similarity(vector1, vector2))
        ret.append(temp)
    return ret


