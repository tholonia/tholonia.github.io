#!/bin/env python

import sys
import getopt
from glob import glob
import re
import itertools
from pprint import pprint

import frontmatter
from spellchecker import SpellChecker
from markdown import markdown
from bs4 import BeautifulSoup

#! for ASNI colors outout
from colorama import init, Fore, Back
init()

def showhelp():
  print("help")
  rs = """
    -h, --help          show help
    -f, --filespec      default: "*.md"
    -r, --recursive     default OFF
    -y, --yaml          include YAML FrontMatter. Default OFF
    -d, --dump          dump bad words only

"""
  print(rs)
  exit()

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

def findintree(filespec):
  allfiles = glob(filespec, recursive=True)  # ! get list of all files
  ab_allfiles = []
  for f in allfiles:  # ! remove all instance of ZPROJECTS, a dir that needs to be ignore.
    if f.find("ZPROJECTS") != -1 or f.find("_site") != -1:
      pass
    else:
      ab_allfiles.append(f)
  found_ary = []
  for file in ab_allfiles:
    found_ary.append(file)
  return found_ary

def load_fm(fn):
  f = open(fn, encoding="utf-8")
  fm = frontmatter.load(f)
  f.close()
  return fm

def markdown_to_text(markdown_string):
  """ Converts a markdown string to plaintext """
  # md -> html -> text since BeautifulSoup can extract text cleanly

  content = markdown(markdown_string.replace("\n", " ").replace("_", " "))
  content = re.sub(r'<pre>(.*?)</pre>', ' ', content)
  content = re.sub(r'<code>(.*?)</code >', ' ', content)


  # extract text

  soup = BeautifulSoup(content, "html.parser")
  text = ''.join(soup.findAll(string=True))

  return text

#! ---------------------------------------------------------------------------
#! Set default values
filespec = "*.md"
recursive = ''
yaml = False
dump = False

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hf:ryd",["help","filespec=","recursive","yaml","dump"],)
except Exception as e:
    print(str(e))

#! set defaults
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-f", "--filespec"): filespec = arg
    if opt in ("-r", "--recursive"): recursive = "**/"
    if opt in ("-y", "--yaml"): yaml = True
    if opt in ("-d", "--dump"): dump = True

#^ ---------------------------------------------------------------------------
#! load the words to ignore
with open('skipwords.txt') as f:
    skipwords = f.read().splitlines()
spell = SpellChecker()
spell.word_frequency.load_words(skipwords)

#! get all files as determined by the arguments
mdfiles = findintree(recursive+filespec)

for file in mdfiles:
  bad_words  = {} #! this holds words that do not exist in the spellchecker or have been listed as incorrect

  # ! load FM and content
  post = load_fm(file)
  content = post.content

  #! this REALLY slows things down
  if yaml:
    import numpy as np
    lst_1d = np.array(post.metadata).flat
    yaml_str = " ".join(map(str, lst_1d))
    content = content + " " +yaml_str

  #! remove any markdown tags other chars and create a list of words
  content = markdown_to_text(content)
  #! Remove URL's. This is here because if there are no HTML stuff BeautifulSoup freaks out
  content = re.sub(r'http\S+', '', content)
  content = re.sub("<[^>]*>", "", content) #! remove HTML tags
  content = re.sub(r' {[%][^}]*[%]}', '', content)  # ! remove LiquidScript tags


  words=spell.split_words(content)

  #! fist make an ary with the bad words using the word as key to eliminate dupe entries
  for word in words:
    if word not in spell.known(word):
      probable_word = spell.correction(word)
      if word != probable_word:
        bad_words[word]=probable_word
  #! test and print
  if len(bad_words) > 0:
    if not dump:
      print(f">>> {Fore.YELLOW}{file}{Fore.RESET}")

  for word in bad_words:
    if word != bad_words[word]:
      if not dump:
        print(f"\t{Fore.GREEN}[{word:20s}]\t{Fore.CYAN}[{bad_words[word]}]{Fore.RESET}")

  #! print our a simple list of bad words for easy cut/paste into skipwords.txt
  if len(bad_words) > 0:
    for w in bad_words:
      print(w)

