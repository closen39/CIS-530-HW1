# Nate Close: closen@seas.upenn.edu

# Import the corpus reader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# lists all sub-directories from this directory
def get_sub_directories(directory):
    return None

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

