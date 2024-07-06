---
layout: post
title: Spellcheck Script
author: duncan
date: 2023-12-30
categories: [BLOG]
tags: [python]
# image: /assets/christmas_miracle.jpg
---
Here's a nifty tool I just banged out that does a spellcheck on every doc.

It's crude, but it works for catching bad words in the file's content and in the YAML metadata if you are checking markdown files.

It's straight forward:

- Get a list of files to check.

- Load each file, extracting a list of words.

- Spellcheck each word, skipping over words it's been told to ignore.

- Print out the misspelled words with correctly spelled suggestion.

However, it will see many bad words if your content and YAML tags are outside the dictionary.  To avoid this, you need to make a file called 'skipwords.txt', which has all the words to ignore.  

To get a list of ONLY the bad words, use the **`-d, --dump`** argument.

If this is run on only a few files, it will be easy to see which words are bad vs. unrecognized.  For many files, it's best to run the scripts on all files, save the output, and create a skipwords.txt file from that output, then rerun the script.

Examples:

`./SPELLCHECK.py -r -y`
- Recursive check all \*.md (default) files from the current working directory.  Include YAML FromtMatter.

`./SPELLCHECK.py -f somedoc.md`

- Check the content only of the file `somedoc.md`.

Here's the code (latest version always [HERE](https://github.com/tholonia/tholonia.github.io/blob/main/SPELLCHECK.py)).  My [skipwords.txt](https://github.com/tholonia/tholonia.github.io/blob/main/src/skipwords.txt) has ~1000 words.  Many of the words are from the Front-matter, which holds YouTube or product ID's, image names, or part of a technical description... that sort of thing, so lots of 'words' like "DzVQqKkT6X0", "e8e4901", "0005s", "2p20", etc.

```python
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
    -v, --verbose       default: OFF

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
  allfiles = glob(filespec, recursive=True) # ! get list of all files
  ab_allfiles = []
  for f in allfiles: # ! remove all instance of ZPROJECTS, a dir that needs to be ignore.
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
verbose = False

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hf:rydv",["help","filespec=","recursive","yaml","dump"],)
except Exception as e:
    print(str(e))

#! set defaults
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-f", "--filespec"): filespec = arg
    if opt in ("-r", "--recursive"): recursive = "**/"
    if opt in ("-y", "--yaml"): yaml = True
    if opt in ("-d", "--dump"): dump = True
    if opt in ("-v", "--verbose"): verbose = True

#^ ---------------------------------------------------------------------------
#! load the words to ignore
with open('skipwords.txt') as f:
    skipwords = f.read().splitlines()
spell = SpellChecker()
spell.word_frequency.load_words(skipwords)

#! get all files as determined by the arguments
mdfiles = findintree(recursive+filespec)

for file in mdfiles:
  bad_words  = {}#! this holds words that do not exist in the spellchecker or have been listed as incorrect

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
  content = re.sub("<[^>]*>", "", content)#! remove HTML tags
  content.replace("%","~")#! need to swap % so it doesn't look like a Liquid command
  content = re.sub(r' {~[^}]*~}', '', content) # ! remove LiquidScript tags


  words=spell.split_words(content)

 #! fist make an ary with the bad words using the word as key to eliminate dupe entries
  for word in words:
    if word not in spell.known(word):
      probable_word = spell.correction(word)
      if word != probable_word:
        bad_words[word]=probable_word
 #! test and print
  if len(bad_words) > 0 or verbose == True:
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


```

