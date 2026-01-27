#!/bin/env python
"""
Read PDF file, limit to 10 srcwords, outpout in FM format
./CATWORD.py -f assets/material/chinese_rainmaking.pdf  -l 10 -s 2

"""

import sys
import os
import getopt
import spacy
import tomllib
import toml
from pprint import pprint
from nltk.stem import WordNetLemmatizer
from colorama import init, Fore, Back
init()

os.environ["SPACY_WARNING_IGNORE"] = "W008" # turn off empty vector warning (doesn't work :/ )

# Load the language model
nlp = spacy.load("en_core_web_lg")


def showhelp():
  print("help")
  rs = """
    -h, --help          show help
    -w, --word          word to classify

"""
  print(rs)
  exit()

def check(word):
  nlp_word = nlp(word)
  for token in nlp_word:
    if token.has_vector == False:
      return 0
  return 1
#^ ---------------------------------------------------------------------------
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hw:",
        ["help","word="],
    )
except Exception as e:
    print(str(e))

#! set defaults
word = False

for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-w", "--word"): word = arg
#^ ---------------------------------------------------------------------------
lemmatizer = WordNetLemmatizer()

if word != False:
  lw = lemmatizer.lemmatize(word)
  print(f"CHECKING: [{lw} ({word})]...",end="")
  results = check(lw)
  if results == 1:
    print(Fore.GREEN+"OK"+Fore.RESET)
  else:
    print(Fore.RED+"NOT OK"+Fore.RESET)
else:
  with open("taxonomy2.toml", mode="rb") as fp:
    config = tomllib.load(fp)

  new_ary = {}
  section = "common"
  ary = config[section]
  for cat in config[section]:
    sary = []
    for w in config[section][cat]:
      lw = lemmatizer.lemmatize(w)
      results = check(lw)
      if results == 1:
        sary.append(lw)
      else:
        pass
      new_ary[cat]=sary
    toml_string = toml.dumps(new_ary)
    print(toml_string)
