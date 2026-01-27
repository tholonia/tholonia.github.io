#!/bin/env python
import os
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
filespec = "**/*.md"

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hf:ydv",["help","filespec="],)
except Exception as e:
    print(str(e))

#! set defaults
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-f", "--filespec"): filespec = arg

#^ ---------------------------------------------------------------------------

os.chdir("/home/jw/sites/tholonia/chirpy2")

#! get all files as determined by the arguments
mdfiles = findintree(filespec)

#! first get all tag/cat pairs
tagcatary = []
for file in mdfiles:
  fm = load_fm(file).metadata
  if 'tags' in fm:
    if 'categories' in fm:
      ftags = fm['tags']
      if type(ftags) != list:
        ftags = [ftags]
      fcats = fm['categories']
      if type(fcats) != list:
        fcats = [fcats]

      try:
        for ftag in ftags:
          for fcat in fcats:
            tagcatary.append([ftag,fcat])
      except:
        tags = []
        cats = []

TAG=0
CAT=1

ucats = []
for i in tagcatary: ucats.append(i[CAT])
utags = []
for i in tagcatary: utags.append(i[TAG])

utags = list(set(utags))
tcary = {}
#! create tag=key array
for uniqt in utags:
  clist = []
  for tcpair in tagcatary:
    # print(f">>> {tcpair[TAG]} == {tcpair[TAG]}")
    if uniqt == tcpair[TAG]:
      clist.append(tcpair[CAT])
  tcary[uniqt]=list(set(clist))

# ! create cat=key array
for t in tcary:
  for c in tcary[t]:
    print(t+","+c)
exit()

ucats = list(set(ucats))
ctary = {}
#! create tag=key array
for uniqc in ucats:
  clist = []
  for tcpair in tagcatary:
    # print(f">>> {tcpair[TAG]} == {tcpair[TAG]}")
    if uniqc == tcpair[CAT]:
      clist.append(tcpair[TAG])
  ctary[uniqc]=list(set(clist))


import json
#! just to examine thge json as an object
# fp = open("mindmap.json","r")
# x = json.load(fp)

mmary = {'class': 'TreeModel',
         'nodeDataArray': [
           {'key': 0,
            'loc': '0 0',
            'text': 'THOLONIA'}
           ]
         }



# pprint(ctary)
# exit()
key = 1
for c in ctary:
  # print(c)
  #! LIST CATS
  attr = {'brush': 'coral',
          'dir': 'left',
          'key': key,
          'loc': '-102.86083984375 130.75',
          'parent': 0,
          'text': c
          }
  sloc = 100
  for t in ctary[c]:
    # print(t)
    # ! LIST CATS
    skey = 1
    sattr = {'brush': 'coral',
            'dir': 'left',
            'key': f"{key}{skey}",
            'loc': f'-150.86083984375 {sloc}',
            'parent': key,
            'text': t
            }
    sloc += 5
    skey += 1
    key += 1
    mmary['nodeDataArray'].append(sattr)
  mmary['nodeDataArray'].append(attr)
# for t in tcary:
#   attr = {'brush': 'coral',
#           'dir': 'right',
#           'key': key,
#           'loc': '-102.86083984375 130.75',
#           'parent': 0,
#           'text': t
#           }
#   mmary['nodeDataArray'].append(attr)

mmjson = json.dumps(mmary)
# pprint(mmary)
print(mmjson)

  # exit()
# ucats = list(set(list(tagcatary.keys())))
#
# for tc in tagcatary:
#
#   print(tc)

# for tc in tagcatary:
#   print(tc)


