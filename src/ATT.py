#!/bin/env python
"""

"""

import sys
import os
import getopt
import spacy
import subprocess

import frontmatter
from pprint import pprint
from glob import glob
import time
from colorama import init, Fore, Back
init()

import locale
print(locale.getpreferredencoding())

timestamp = time.time()

def showhelp():
  print("help")
  rs = """
    -h, --help          show help

"""
  print(rs)
  exit()

def tryit(kwargs, arg, default):
  try:
    rs = kwargs[arg]
  except:
    rs = default
  return rs


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
    if f.find("ZPROJECTS") != -1 or f.find("_site") != -1:
      pass
    else:
      ab_allfiles.append(f)

  # ! the following only works if the PDF filename is a unique part of the MD filename
  nameparts = split_path(filename)
  found_ary = []
  # pprint(ab_allfiles)
  for file in ab_allfiles:
    found_ary.append(file)
  return found_ary

def load_fm(fn):

  f = open(fn, encoding="utf-8")
  fm = frontmatter.load(f)
  f.close()
  return fm

def getyaml(file):
  post = load_fm(file)          #! load FM and content
  return post.metadata

class easystr(str):
  def decode(self):
    return str.decode(self, errors="ignore")

#! ---------------------------------------------------------------------------
#! ---------------------------------------------------------------------------
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "h",
        ["help"],
    )
except Exception as e:
    print(str(e))

#! set defaults
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()


#^ ---------------------------------------------------------------------------
#^ ---------------------------------------------------------------------------

mdfiles = findintree("*md")

tagct = {}
catct = {}

for file in mdfiles:
  print(file)
  post = load_fm(file)          #! load FM and content
  try:
    tags = post.metadata['tags']
    if isinstance(tags,list):
      for tag in tags:
        if tag in tagct:
          tagct[tag] = tagct[tag]+1
        else:
          tagct[tag] =1
    else:
      if tags in tagct:
        tagct[tags] = tagct[tags] + 1
      else:
        tagct[tags] = 1
  except:
    pass
  for yaml in post.metadata:
    # pass
    print(f"\t{Fore.GREEN}{yaml:20s}{Fore.RESET}", end="")
    print(f"\t{Fore.RED}{post.metadata[yaml]}{Fore.RESET}")
  # pprint(tagct)

  # by value
tags_key = dict(sorted(tagct.items(), key=lambda item: item[0]))
print(Fore.GREEN)
for t in tags_key:print(f"{t:20s}{tags_key[t]}")
print(Fore.RESET)


tags_value = dict(sorted(tagct.items(),  key=lambda item: item[1]))
# tags_value = {k: v for k, v in sorted(tagct.items(), key=lambda item: item[1])}

print(Fore.YELLOW)
for t in tags_value:print(f"{t:20s}{tags_value[t]}")
print(Fore.RESET)

#! cats


for file in mdfiles:
  print(file)
  post = load_fm(file)          #! load FM and content
  try:
    cats = post.metadata['categories']
    if isinstance(cats,list):
      for cat in cats:
        if cat in catct:
          catct[cat] = catct[cat]+1
        else:
          catct[cat] =1
    else:
      if cats in catct:
        catct[cats] = catct[cats] + 1
      else:
        catct[cats] = 1
  except:
    pass
  for yaml in post.metadata:
    # pass
    print(f"\t{Fore.GREEN}{yaml:20s}{Fore.RESET}", end="")
    print(f"\t{Fore.RED}{post.metadata[yaml]}{Fore.RESET}")

  # by value

pprint(catct)
cats_key = dict(sorted(catct.items(), key=lambda item: item[0]))
print(Fore.GREEN)
for t in cats_key:print(f"{t:20s}{cats_key[t]}")
print(Fore.RESET)


cats_value = dict(sorted(catct.items(),  key=lambda item: item[1]))

print(Fore.YELLOW)
for t in cats_value:print(f"{t:20s}{cats_value[t]}")
print(Fore.RESET)
