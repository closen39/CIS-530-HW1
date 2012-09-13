# Nate Close: closen@seas.upenn.edu

# Import the corpus reader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize

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
    sent = ''
    for line in file1:
        sent = sent + line
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

