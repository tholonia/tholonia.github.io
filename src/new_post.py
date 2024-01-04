#!/bin/env python


import sys,os
import getopt
from pprint import pprint
import frontmatter
from markdown import markdown
import datetime
import time
import shutil

#! for ASNI colors outout
from colorama import init, Fore, Back
init()

os.chdir("/home/jw/sites/tholonia/chirpy2")
print("cwd: /home/jw/sites/tholonia/chirpy2")

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

def showhelp():
  print("help")
  rs = """
    -h, --help          show help
    -v, --verbose
  ` -D, --dryrun        show commands, don't run them
    if opt in ("-c", "--cats"): cats = arg
    if opt in ("-t", "--tags"): tags = arg
    if opt in ("-i", "--img"): img = arg
    if opt in ("-p", "--pdf"): pdf = arg
    if opt in ("-T", "--title"): title = arg
    isbook False

./new_material.py \
    -c "GEOSCIENCE,NATURE,METAPHYSICS" \
    -t "water" \
    -i /home/jw/store/sites/tholonia/chirpy2/assets/2024-04-01-healing-with-water/Healing-With-Water.jpg \
    -p /home/jw/store/sites/tholonia/chirpy2/assets/2024-04-01-healing-with-water/Healing-With-Water.pdf \
    -T "Healing with Water"

"""
  print(rs)
  exit()

def load_fm(fn):

  f = open(fn, encoding="utf-8")
  fm = frontmatter.load(f)
  f.close()
  return fm
#^ ---------------------------------------------------------------------------
#! Set default values
verbose = False

cats = False
date = False
img = False
jday = False
pdf = False
tags = False
title=False
pretext = False
posttext = False
dryrun = False

argv = sys.argv[1:]
# print(sys.argv)

try:
    opts, args = getopt.getopt(argv,"hvc:t:i:p:T:D",["help","verbose","cats=","tags=","img=","pdf=","title=","dryrun"])
except Exception as e:
    print(str(e))

#! set defaults
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-v", "--verbose"): verbose = True
    if opt in ("-c", "--cats"): cats = arg
    if opt in ("-t", "--tags"): tags = arg
    if opt in ("-i", "--img"): img = arg
    if opt in ("-p", "--pdf"): pdf = arg
    if opt in ("-T", "--title"): title = arg
    if opt in ("-D", "--dryrun"): dryrun = True

#^ ---------------------------------------------------------------------------
def make_newfn(fn,outfilename):
  outfilename = outfilename.replace(".md","")
  iparts = split_path(fn)
  newfn = f"{loc_asset}/{outfilename}/post_image.{iparts['ext']}"
  if not os.path.exists(f"{loc_asset}/{outfilename}"):
    os.mkdir(f"{loc_asset}/{outfilename}")
  return(newfn)
def urlify(str):
  str = str.replace("/home/jw/store/sites/tholonia/chirpy2","")
  str = str.replace("/_material","/material")
  return(str)
loc_md = "/home/jw/store/sites/tholonia/chirpy2/_posts"
loc_asset = "/home/jw/store/sites/tholonia/chirpy2/assets/posts"

fm = load_fm("/home/jw/store/sites/tholonia/chirpy2/docs/_post_template.md")

tdate = str(datetime.date.today())
# jday = int(time.time()/86400)
text = "\n<!--more-->\n"

if title == False: title = input("title: [SKIP]: ").strip() or "SKIP"
fn = title.lower().replace(" ","-")
outfilename = f"{tdate}-{fn}.md"

if cats == False: cats = input("categories: [CAT1,CAT2]: ").strip() or "CAT1,CAT2"
if tags == False: tags = input("tags: [TAG1,TAG2]: ").strip() or "TAG1,TAG2"
if img == False: img = input("image: [SKIP]: ").strip() or "SKIP"
newimg = make_newfn(img,outfilename)

fm.metadata['categories']=cats.split(",")
fm.metadata['date']=tdate
fm.metadata['tags']=tags.split(",")
fm.metadata['image']=urlify(newimg)
fm.metadata['title']=title
# fm.metadata['jday']=jday

print(Fore.WHITE+"OUTPUT FILE: [{loc_md}/{outfilename}]"+Fore.RESET)

for m in fm.metadata:
  print(Fore.CYAN+f"{m:15s}"+Fore.YELLOW+f"{fm.metadata[m]}"+Fore.RESET)

isok = input("OK? [y/N]").strip() or "N"
if isok != "y":
  exit()

if img != False:
  try:
    print(">>> "+Fore.YELLOW+f"mv {img} {newimg}"+Fore.RESET)
    if dryrun == False and  img != newimg:
      shutil.move(img,newimg)
  except:
    print ("skipping image")
    img += " MISSING"
  fm.metadata['image']=urlify(newimg)

fm.content = text
final = frontmatter.dumps(fm)  # ! write back to file

print(Fore.GREEN+final+Fore.RESET)
if dryrun == False:
  with open(f"{loc_md}/{outfilename}", 'w', encoding="utf-8") as f:
    f.write(final)
  f.close()

print(Fore.WHITE+f"{loc_md}/{outfilename}")

#!  now move everythign to teh right place

