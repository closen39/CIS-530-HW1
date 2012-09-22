# Nate Close: closen@seas.upenn.edu
# Jason Mow: jmow@seas.upenn.edu

# Import the corpus reader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

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
        for f in files:
            for word in load_collection_tokens(path):
                fdist.inc(word)  
    li = fdist.keys()
    return li[:n]
