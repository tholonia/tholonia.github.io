#!/bin/env python


import sys,os
import getopt
from pprint import pprint
import frontmatter
from markdown import markdown
import datetime
import time
import shutil
from PIL import Image

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
  ` -D, --dryrun      show commands, don't run them
    -c, --cats        cat1[,cat2]  no spaces
    -t, --tags        tag1[,tag2]  no spaces
    -i, --img         path to image
    -p, --pdf         path to pdf
    -T, --title       "Title Words"
    -b,  -isbook      use for book default = material

Example
./new_material.py \\
    -c "GEOSCIENCE,NATURE,METAPHYSICS" \\
    -t "water" \\
    -i /home/jw/Healing-With-Water.jpg \\
    -p /home/jw//Healing-With-Water.pdf \\
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
is_book = False
dryrun = False

argv = sys.argv[1:]
# print(sys.argv)

try:
    opts, args = getopt.getopt(argv,"hvc:t:i:p:T:bD",["help","verbose","cats=","tags=","img=","pdf=","title=","isbook","dryrun"])
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
    if opt in ("-b", "--isbook"): is_book = True
    if opt in ("-D", "--dryrun"): dryrun = True

#^ ---------------------------------------------------------------------------
def make_newfn(fn,outfilename):
  outfilename = outfilename.replace(".md","")
  iparts = split_path(fn)
  newfn = f"{loc_asset}/{outfilename}.{iparts['ext']}"

  if is_book == True:
    newfn =  "https://tholonia.github.io"+newfn
    newfn.replace(".pdf",".zip")

  return(newfn)
def urlify(str):
  str = str.replace("/home/jw/store/sites/tholonia/chirpy2","")
  str = str.replace("/_material","/material")
  return(str)

#! don't need this for webp.  Maybe fopr resize or png ?
def mvc(img,newimg):
  trximg = img
  iparts = split_path(img)
  if iparts['ext'] == "webp":
    im = Image.open(img).convert("RGB")
    trximg = f"{iparts['dirname']}/{iparts['basename']}.jpg"
    print(f">>> converted [{img}] to [{trximg}]")
    im.save(newimg,"jpeg")
  shutil.move(trximg,newimg)
  return(trximg)

loc_md = "/home/jw/store/sites/tholonia/chirpy2/_material"
loc_asset = "/home/jw/store/sites/tholonia/chirpy2/_material/assets"

fm = load_fm("/home/jw/store/sites/tholonia/chirpy2/docs/_material_template.md")

tdate = str(datetime.date.today())
# jday = int(time.time()/86400)
text = "\n<!--more-->\n"

if title == False: title = input("title: [SKIP]: ").strip() or "SKIP"
fn = title.lower().replace(" ","-")
if is_book == True:
  outfilename = f"book_{fn}.md"
else:
  outfilename = f"material_{fn}.md"

if cats == False: cats = input("categories: [CAT1,CAT2]: ").strip() or "CAT1,CAT2"
if tags == False: tags = input("tags: [TAG1,TAG2]: ").strip() or "TAG1,TAG2"
if img == False: img = input("image: [SKIP]: ").strip() or "SKIP"
newimg = make_newfn(img,outfilename)
if pdf == False: pdf = input("pdf: [SKIP]: ").strip() or "SKIP"
newpdf = make_newfn(pdf,outfilename)

fm.metadata['categories']=cats.split(",")
fm.metadata['date']=tdate
fm.metadata['tags']=tags.split(",")
fm.metadata['image']=urlify(newimg)
fm.metadata['pdf']=urlify(newpdf)
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
      #! newimg = mvc(img,newimg)   dont need for webp. maybe png?
      shutil.move(img, newimg)
  except:
    print ("skipping image")
    img += " MISSING"
  fm.metadata['image']=urlify(newimg)

if pdf != False:
  try:
    print(">>> "+Fore.YELLOW+f"mv {pdf} {newpdf}"+Fore.RESET)
    if dryrun == False and pdf != newpdf:
      shutil.move(pdf,newpdf)
  except:
    pdf += " MISSING"
    print ("skipping PDF")

  fm.metadata['pdf']=urlify(newpdf)
  text += "\n{% include pdf-download-obj.html %}"

fm.content = text
final = frontmatter.dumps(fm)  # ! write back to file

print(Fore.GREEN+final+Fore.RESET)
if dryrun == False:
  with open(f"{loc_md}/{outfilename}", 'w', encoding="utf-8") as f:
    f.write(final)
  f.close()

print(Fore.WHITE+f"{loc_md}/{outfilename}")

#!  now move everythign to teh right place

