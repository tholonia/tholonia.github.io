#!/bin/env python
"""
Read PDF file, limit to 10 srcwords, outpout in FM format
./CATWORD.py -f assets/material/chinese_rainmaking.pdf  -l 10 -s 2

"""

import sys
import os
import getopt
import spacy
spacy.require_gpu(0)
import nltk
# nltk.download('averaged_perceptron_tagger')
import tomllib
from keybert import KeyBERT
from tika import parser
import tika
tika.initVM()
from nltk.stem import WordNetLemmatizer
import transformers
import torch
import frontmatter
from pprint import pprint
from glob import glob
import time
from colorama import init, Fore, Back
init()

os.environ["SPACY_WARNING_IGNORE"] = "W008" # turn off empty vector warning (doesn't work :/ )

# Load the language model
nlp = spacy.load("en_core_web_lg")


def showhelp():
  print("help")
  rs = f"""
    -h, --help          show help
    -w, --word          word to classify          (required)
    -s, --simple        1=text, 2=FrontMatter     (def: 1)
    -t, --taxonomy      'relevant' or 'common'    (def: relevant)
    -l, --limit         max src words             (def: 10000)
    -v, --verbose       show information          (def: False)

    example {__file__} --word baseball  --limit 10  ---verbose
"""
  print(rs)
  exit()

def getroot(words):
  lemmatizer = WordNetLemmatizer()
  nw = []
  for w in words:
    rw = lemmatizer.lemmatize(w)
    nw.append(rw)
  return(nw)

def getUniqueWords(allWords):
  uniqueWords = []
  for i in allWords:
    if not i in uniqueWords:
      uniqueWords.append(i)
  return uniqueWords

def getarg(kwargs, arg, default):
  try:
    rs = kwargs[arg]
  except:
    rs = default
  return rs

def Average(lst):
  return sum(lst) / len(lst)

def locate_ary(word,words):
  sim_ary = []
  for w in words:
    # Process the sentences using spaCy
    doc1 = nlp(word)
    doc2 = nlp(w)

    # Compute the similarity between the two sentences
    similarity = doc1.similarity(doc2)
    sim_ary.append(f"{similarity:02.3F}")
  return sim_ary

def nlpize(word,cat):
  nlp_word = nlp(word)
  for token in nlp_word:
    if token.has_vector == False:
      if verbose == True:
        print(f"{cat}:[{word}] is not recognized by this model")
      return False
  return nlp_word

#! tokenize new_word, then loop through tokenized src-words and add the similarity
#! values to an array that is averaged.
def locate_avg(newword,srcwords,**kwargs):
  cat = getarg(kwargs,"cat",False)
  sim_ary = []
  nlp_newword = nlpize(newword,cat)
  if nlp_newword != False:
    for srcword in srcwords:
      #! Process the sentences using spaCy
      nlp_srcword = nlpize(srcword,cat)
      if nlp_srcword != False:
        for token in nlp_srcword:
          if(token and token.vector_norm):
            similarity = nlp_newword.similarity(nlp_srcword)
            sim_ary.append(similarity)
    return Average(sim_ary)
  else:
    return False

#! loop through list of key values in the taxonomy and send the new word
#! and list of src words to the averager
def avgword(word,config):
  results = []
  for CAT in config[taxonomy]:
    list_of_words =  config[taxonomy][CAT][:limit]
    avg_results = locate_avg(word,list_of_words,cat=CAT)
    if avg_results != False:
      results.append([word, f"{CAT:20s}", avg_results])
    else:
      return False
  results.sort(key=lambda x: x[2])
  return results[::-1]

def get_keywords_bert(fn):
  print("Keyword Extraction: RoBert")

  raw = parser.from_file(fn)
  def check(word):
    # print(f"checking {word}")
    nlp_word = nlp(word)
    for token in nlp_word:
      if token.has_vector == False:
        return 0
    return 1
  #! Tested only with PDF and TXT !
  # raw = parser.from_file('/home/jw/store/sites/tholonia/chirpy2/assets/material/Introduction_to_Complex_Systems_Sustainability_and.pdf')
  raw = parser.from_file(fn)
  doc = raw['content']

  #! comparison test - no obv diff, but much slower and needs a tika-server :/
  kw_model = KeyBERT()
  try:
    keywords = kw_model.extract_keywords(doc)
    # keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), stop_words=None)
    # keywords = kw_model.extract_keywords(doc, highlight=True)

    cleaned_kw = []
    for k in keywords:
      if check(k[0]) == 1:
        cleaned_kw.append(k)
      else:
        print(f"Removing {Fore.RED}[{k}]{Fore.RESET}")
    return cleaned_kw
  except:
    return False

def split_path(pstr):
  dirname = os.path.dirname(pstr)

  if dirname == "" or dirname == ".":
    dirname = os.getcwd()
  basename = os.path.basename(pstr)
  ns = basename.split(".")
  ext = ns[-1]
  nameonly = "".join(ns[:-1])
  fullpath = f"{dirname}/{basename}"

  return {
    "dirname": dirname,
    "basename": basename,
    "ext": ext,
    "nameonly": nameonly,
    "fullpath": fullpath,
  }
def findintree(filename):
  # ! update FrontMatter file
  allfiles = glob("**/*.md", recursive=True)  # ! get list of all files
  ab_allfiles = []
  for f in allfiles:  # ! remove all instance of ZPROJECTS, a dir that needs to be ignore.
    if f.find("ZPROJECTS") != -1:
      pass
    else:
      ab_allfiles.append(f)

  # ! the following only works if the PDF filename is a unique part of the MD filename
  nameparts = split_path(filename)
  searchterm = nameparts['nameonly']
  found_ary = []
  for file in ab_allfiles:
    # print(Fore.YELLOW+f"Searching for [{searchterm}] in [{file}]"+Fore.RESET)
    if file.find(searchterm) != -1:
      found_ary.append(file)
  return {'found_ary':found_ary,'searchterm':searchterm}

def load_fm(fn):
  with open(fn) as f:
      return frontmatter.load(f)

def updateFM(files,simple,rutags,ucats):
  for file in files:
    post = load_fm(file)          #! load FM and content
    post.metadata['tags'] = rutags      #! update tags
    post.metadata['categories'] = ucats #! update cats
    final = frontmatter.dumps(post)     #! write back to file
    with open(file, 'w') as f:
      f.write(final)

def test_fm_tag(file,tag,value):
  post = load_fm(file)
  try:
    if value in post.metadata['ptags']:
      return True
  except:
    return False
  return False

#! ---------------------------------------------------------------------------
#! ---------------------------------------------------------------------------
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hw:s:t:l:vf:r",
        ["help","word=","simple","taxonomy=","limit=","verbose","filename=","report"],
    )
except Exception as e:
    print(str(e))

#! set defaults
word = False
filename = False
simple = False
taxonomy = "relevant"
limit = 10000
verbose = False
similarity_minimum=0.3 #! must have at least 30% similarity
report = False

for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-w", "--word"): word = arg
    if opt in ("-s", "--simple"): simple = int(arg)
    if opt in ("-t", "--taxonomy"): taxonomy = arg
    if opt in ("-l", "--limit"): limit = int(arg)
    if opt in ("-v", "--verbose"): verbose = True
    if opt in ("-f", "--filename"): filename = arg
    if opt in ("-r", "--report"): report = True
#^ ---------------------------------------------------------------------------
#^ ---------------------------------------------------------------------------
if filename != False:
  border = f"""
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │   STARTING:   {filename:96s}│
  └───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
  """
  print(Fore.CYAN+border+Fore.RESET)
starttime = time.time()



with open("taxonomy2.toml", mode="rb") as fp:
  config = tomllib.load(fp)

#! report count for each catagory
if report == True:
  for cat in config[taxonomy]:
    print(f"{cat}: {len(config[taxonomy][cat])}")
  exit()

#! first check if we have an output file available if simple=2

keywords = [(word,1.0)] #! make a fake keyword tuple

for kw in keywords:
  if kw[1] > similarity_minimum: #! must have at least 30% similarity
    results = avgword(kw[0],config)
    if results != False:
      if simple == 1:
        print(Fore.CYAN+results[0]+Fore.RESET)
      else:
        for r in results:
          print(r)


endtime = time.time()

elapsed = (endtime - starttime)/60

print(f'Time taken: {Fore.LIGHTWHITE_EX}{elapsed:3.1f}{Fore.RESET} minutes')

