#!/bin/env python
"""
Read PDF file, limit to 10 srcwords, outpout in FM format

"-s 2" required to update markdown file

./CATFILE.py -f chinese_rainmaking.pdf -l 10 -s 2

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
import PyPDF2
import subprocess

# from keyphrase_vectorizers import KeyphraseCountVectorizer
import torch
import frontmatter
import frontmatter
from pprint import pprint
from glob import glob
import time
from colorama import init, Fore, Back
init()

import locale
print(locale.getpreferredencoding())

os.environ["SPACY_WARNING_IGNORE"] = "W008" # turn off empty vector warning (doesn't work :/ )

# Load the language model
nlp = spacy.load("en_core_web_lg")

timestamp = time.time()

os.chdir("/home/jw/sites/tholonia/chirpy2")

def showhelp():
  print("help")
  rs = """
    -h, --help          show help
    -s, --simple        1=text, 2=FrontMatter
    -t, --taxonomy      'relevant' or 'common'
    -l, --limit         max src words to compare keyword against
    -v, --verbose       show information
    -f, --filename      PDF file to parse
  Do NOT use teh following flags
    -w, --word          keyword to classify
    -k, --numkeys       number of keywords

"""
  print(rs)
  exit()

def tryit(kwargs, arg, default):
  try:
    rs = kwargs[arg]
  except:
    rs = default
  return rs


def getroot(words,**kwargs):
  km_ary = tryit(kwargs,'km_ary',False)
  lemmatizer = WordNetLemmatizer()
  if km_ary == True:
    c2ary=[]
    for k in words:
      c2ary.append( (lemmatizer.lemmatize(k[0]),k[1]) )
    words=c2ary
    return words
  else:
    # print("XXX-1",words)
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

def prunlive(cmd, **kwargs):
  # print("+++++++++++++",cmd)
  debug = tryit(kwargs, "debug", False)
  dryrun = tryit(kwargs, "dryrun", False)
  # cmd = str(cmd).replace("~","\xC2\xA0")
  if dryrun == "print":
    print(Fore.YELLOW + cmd + Fore.RESET)
    return

  # cmd = cmd.replace("~", "X")
  # cmd = cmd.replace("~", "\u00A0")
  scmd = cmd.split()
  # print("===========", scmd)
  for i in range(len(scmd)):
    scmd[i] = scmd[i].replace("~", " ")
    scmd[i] = scmd[i].replace('"', "")
  if debug:
    print(Fore.YELLOW + cmd + Fore.RESET)
    # pprint(scmd)

  process = subprocess.Popen(scmd, stdout=subprocess.PIPE)
  for line in process.stdout:
    print(Fore.RED)
    sys.stdout.write(line.decode("utf-8"))
    print(Fore.RESET)


def get_keywords_nltk(fn):
  print("Keyword Extraction: NLTK")
  headers = {
    "X-Tika-OCRLanguage": "eng",
    "X-Tika-PDFocrStrategy": "OCR_AND_TEXT_EXTRACTION"
  }
  os.environ['TIKA_SERVER_ENDPOINT'] = 'https://0.0.0.0:9998/'

  #! strip leading _ for url compatibility
  # fn = f"https://0.0.0.0:9998/{fn[1:]}"
  # print(f"XXX: about to read file {fn}")
  text = parser.from_file(f"{fn}",xmlContent=False, requestOptions={'headers':headers,'timeout':300})
  # text = parser.from_file("/home/jw/sites/tholonia/chirpy2/_material/assets/Chemical_Evolution.pdf", xmlContent=False, requestOptions={'headers': headers, 'timeout': 300})
  # print("XXX:",text)

  #^ from https://spotintelligence.com/2022/12/13/keyword-extraction/#:~:text=SpaCy%20keyword%20extraction,-Here%20is%20an&text=This%20example%20first%20loads%20the,phrases%20according%20to%20their%20importance.
  #! Preprocess the text by removing punctuation and converting to lowercase
  text = text['content'] .lower().replace(".", "")

  #! Tokenize the text into words
  tokens = nltk.word_tokenize(text)

  #! Use part-of-speech tagging to identify the nouns in the text
  tags = nltk.pos_tag(tokens)
  nouns = [word for (word, tag) in tags if tag == "NN"]

  #! Use term frequency-inverse document frequency (TF-IDF) analysis to rank the nouns
  from sklearn.feature_extraction.text import TfidfVectorizer
  vectorizer = TfidfVectorizer()
  tfidf = vectorizer.fit_transform([text])

  # Get the top 3 most important nouns
  top_nouns = sorted(vectorizer.vocabulary_, key=lambda x: tfidf[0, vectorizer.vocabulary_[x]], reverse=True)[:3]

  # Print the top 3 keywords
  print(top_nouns)

def get_keywords_spacy(fn):
  print("Keyword Extraction: SpaCy")

  raw = parser.from_file(fn)
  #! Load the Spacy model and create a new document
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(raw['content'])

  #! Use the noun_chunks property of the document to identify the noun phrases in the text
  noun_phrases = [chunk.text for chunk in doc.noun_chunks]

  #! Use term frequency-inverse document frequency (TF-IDF) analysis to rank the noun phrases
  from sklearn.feature_extraction.text import TfidfVectorizer
  vectorizer = TfidfVectorizer()
  tfidf = vectorizer.fit_transform([doc.text])

  #! Get the top 3 most important noun phrases
  top_phrases = sorted(vectorizer.vocabulary_, key=lambda x: tfidf[0, vectorizer.vocabulary_[x]], reverse=True)[:3]

  #! Print the top 3 keywords
  print(top_phrases)
  exit()


def get_keywords_bert2(fn):
  print("Keyword Extraction: RoBert 2")
  raw = parser.from_file(fn)

  #! Load the BERT model and create a new tokenizer
  model = transformers.BertModel.from_pretrained("bert-base-uncased")
  tokenizer = transformers.BertTokenizer.from_pretrained("bert-base-uncased")

  #! Tokenize and encode the text
  input_ids = tokenizer.encode(raw['content'], add_special_tokens=True)

  #! Use BERT to encode the meaning and context of the words and phrases in the text
  outputs = model(torch.tensor([input_ids]))

  #! Use the attention weights of the tokens to identify the most important words and phrases
  attention_weights = outputs[-1]
  top_tokens = sorted(attention_weights[0], key=lambda x: x[1], reverse=True)[:3]

  #! Decode the top tokens and print the top 3 keywords
  top_keywords = [tokenizer.decode([token[0]]) for token in top_tokens]
  print(top_keywords)

def get_keywords_bert(fn):
  print(f"Keyword Extraction: RoBert ({fn})")

  # raw = parser.from_file(fn)['content']

  # pprint(raw)
  # exit()
  def check(word):
    # print(f"checking {word}")
    nlp_word = nlp(word)
    for token in nlp_word:
      if token.has_vector == False:
        return 0
    return 1
  #! tested on PDF and TXT only!
  raw = parser.from_file(fn)
  doc = raw['content'][2300:]

  kw_model = KeyBERT()
  #! comparison test - no obv diff, but much slower and needs a tika-server :/
  try:
    keywords = kw_model.extract_keywords(doc, top_n=numkeys, use_mmr=True)
    # keywords = kw_model.extract_keywords(doc, top_n=numkeys)

    # keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), stop_words=['copyright','publishing','publish'])
    # keywords = kw_model.extract_keywords(doc, highlight=True)
    # xxx=" AI entity We traditionally define intelligence as The ability to learn understand and make managed pest control as they use no chemical"
    # keywords = kw_model.extract_keywords(xxx, highlight=True)

    keywords = getroot(keywords,km_ary=True)
    # pprint(keywords)

    # exit()

    cleaned_kw = []
    for k in keywords:
      if check(k[0]) == 1:
        cleaned_kw.append(k)
      else:
        print(f"Removing {Fore.RED}[{k}]{Fore.RESET}")


    return cleaned_kw
  except Exception as e:
    print("Failed getting keywords)")
    print(e.str)
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
  # pprint(ab_allfiles)
  for file in ab_allfiles:
    # print(Fore.YELLOW+f"Searching for [{searchterm}] in [{file}]"+Fore.RESET)
    if file.find(searchterm) != -1:
      found_ary.append(file)
  return {'found_ary':found_ary,'searchterm':searchterm}

def load_fm(fn):

  f = open(fn, encoding="utf-8")
  fm = frontmatter.load(f)
  f.close()
  return fm

def updateFM(files,simple,rutags,ucats):
  for file in files:
    post = load_fm(file)          #! load FM and content
    post.metadata['tags'] = rutags      #! update tags
    post.metadata['categories'] = ucats #! update cats
    final = frontmatter.dumps(post)     #! write back to file
    with open(file, 'w', encoding="utf-8") as f:
      f.write(final)

def test_fm_tag(file,tag,value):
  post = load_fm(file)
  try:
    ptags = post.metadata[tag]
    if str(ptags).find(value) != -1:
      return ptags
  except:
    return False
  return False

class easystr(str):
  def decode(self):
    return str.decode(self, errors="ignore")

#! ---------------------------------------------------------------------------
#! ---------------------------------------------------------------------------
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hw:s:t:l:vf:rk:",
        ["help","word=","simple","taxonomy=","limit=","verbose","filename=","report","numkeys="],
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
numkeys = 4
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-w", "--word"): word = arg
    if opt in ("-s", "--simple"): simple = int(arg)
    if opt in ("-t", "--taxonomy"): taxonomy = arg
    if opt in ("-l", "--limit"): limit = int(arg)
    if opt in ("-v", "--verbose"): verbose = True
    if opt in ("-f", "--filename"): filename = arg
    if opt in ("-r", "--report"): report = True
    if opt in ("-k", "--numkeys"): numkeys = int(arg)


#^ ---------------------------------------------------------------------------
#^ ---------------------------------------------------------------------------
if filename != False:
  border = f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │   STARTING:   {filename:96s}│
  └──────────────────────────────────────────────────────────────────┘
  """
  print(Fore.CYAN+border+Fore.RESET)
starttime = time.time()



with open("/home/jw/sites/tholonia/chirpy2/src/taxonomy2.toml", mode="rb") as fp:
  config = tomllib.load(fp)

#! report count for each catagory
if report == True:
  for cat in config[taxonomy]:
    print(f"{cat}: {len(config[taxonomy][cat])}")
  exit()

#! first check if we have an output file available if simple=2

if simple == 2:
  testtarget = findintree(filename)
  found_files = testtarget['found_ary']
  if len(testtarget['found_ary']) < 1:
    print(f"No target Found searching for [{testtarget['searchterm']}]")
    exit()
  else:
      for file in found_files:
        print(Fore.YELLOW+f"Found [{file}]"+Fore.RESET+" ...updating...")
      # ! first check FM for ptag="nokwgen"
      flagged = test_fm_tag(file,"ptags","nokwgen")
      if flagged:
        print(Fore.RED+f"Flagged as '{flagged}'"+Fore.RESET)
      else:
        if filename == False: #! if not filename given, assume 'word' has been explicitly assigned
          keywords = [(word,1.0)] #! make a fake keyword tuple
        else:
          # keywords = get_keywords_nltk(filename)
          keywords = get_keywords_bert(filename)
          # keywords = get_keywords_bert2(filename) # broken
          # keywords = get_keywords_spacy(filename)
          if verbose:
            print(Fore.WHITE+ "FOUND KEYWORDS"+Fore.RESET)
            for k in keywords:
              print(f"{Fore.GREEN}{k[0]:20s}{Fore.CYAN}{k[1]:5.4f}{Fore.RESET}")

        #! del any existing temp files
        if os.path.exists("/tmp/kw.txt"):
          os.unlink("/tmp/kw.txt")

        if keywords != False:
          for kw in keywords:
            if kw[1] > similarity_minimum: #! must have at least 30% similarity
              results = avgword(kw[0],config)
              if results != False:
                if simple == 1:
                  print(results[0])
                elif simple == 2:
                  with open("/tmp/kw.txt", mode="a") as fp: #! save output to file for later processing
                    fp.write(f"{kw[0]},{results[0][1]}\n")
                else:
                  for r in results:
                    print(r)

          tag_ary = []
          cat_ary = []
          #! if /tmp/kw.txt exists then we have set s=2 option
          if os.path.exists("/tmp/kw.txt"):
            with open("/tmp/kw.txt") as fp:
              for line in fp.readlines(): #! create lists of tags abd cats
                lp = line.split(",")
                tag_ary.append(lp[0].strip("\n").strip()) #! remove newline and trailing whitespace
                cat_ary.append(lp[1].strip("\n").strip())

              rutags = getroot(tag_ary)       #! reduce word to base.. doesn't really do much... removes plurals only
              # rutags = tag_ary  #! getroot mangles too many words, like 'mars' -> 'mar' !?
              utags = getUniqueWords(rutags) #! remove all dupes
              ucats = getUniqueWords(cat_ary)

              # print(Fore.RED + f"{utags}" + Fore.RESET)
              # print(Fore.GREEN + f"{rutags}" + Fore.RESET)

              # print(Fore.CYAN+filename+Fore.RESET)
              print(Fore.LIGHTGREEN_EX+f"tags: [{','.join(utags)}]"+Fore.RESET)
              print(Fore.LIGHTGREEN_EX+f"categories: [{','.join(ucats)}]"+Fore.RESET)
              # found_files = findintree(filename)
              # for file in found_files:
              #   print(Fore.YELLOW+f"Found [{file}]"+Fore.RESET+" ...updating...")
              updateFM(found_files,simple,rutags,ucats)
          else:
            if simple == 2:
              print(Fore.LIGHTRED_EX+f"/tmp/kw.txt DOES NOT EXISTS - Keywords all below {similarity_minimum} similarity"+Fore.RESET)
              fo = open("nokw.txt","a")
              fo.write(f"{timestamp}: joe {filename}\n")
              fo.close()

endtime = time.time()

elapsed = (endtime - starttime)/60

print(f'Time taken: {Fore.LIGHTWHITE_EX}{elapsed:3.1f}{Fore.RESET} minutes')

# border = f"""
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
# """
# print(Fore.MAGENTA+border+Fore.RESET)
