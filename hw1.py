# Nate Close: closen@seas.upenn.edu

# Import the corpus reader
from nltk.corpus import PlaintextCorpusReader

# lists all sub-directories from this directory
def get_sub_directories(directory):
    return None

# gets all files in this directory and its sub-directories
def get_all_files(directory):
  files = PlaintextCorpusReader(directory, '.*')
  return files.fileids() 

# returns a list of all sentences in that file
def load_file_sentences(filepath):
    return None

# load all sentences in files within this drectory
# should return list of sentences
def load_collection_sentences(directory):
    return None

