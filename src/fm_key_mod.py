#!/bin/env python
"""
update tags or cats in frontmatter
"""

import glob
from datetime import datetime, timedelta
import frontmatter
import os, sys, getopt
from pprint import pprint
from colorama import init, Fore, Back
init()

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
  rs = f"""
    -h, --help          show help
    -f, --filename      PDF file to parse
    -k, --fmkey         frontmatter key name
    -F, --fromval       existing value
    -T, --toval         new value
    -v, --verbose       show information

    Currently only work on FM kets that hold (or can hold) arrays.

    Example:
    Change the value of VIDEOS in 'categories' to anotehr value.  If the new value is '86'
    the old value simple deleted.

    {__file__} -filename _videos/ -fmkey categories -frmval VIDEOS -toval 86
    {__file__} -f _videos/ -k categories -F VIDEOS -T 86

"""
  print(rs)
  exit()


def get_key(k,post):
  try:
    v = post.metadata[k]
    return v
  except:
    return False

def snr_ary(fr,to,ary):
  for i, n in enumerate(ary):
    if n == fr:
      ary[i] = to
    return ary

def show(data, clr):
  print(clr)
  pprint(data)
  print(Fore.GREEN)
#! ---------------------------------------------------------------------------
#! ---------------------------------------------------------------------------
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hf:k:F:T:vD",
        ["help","filename=","fmkey","fromval=","toval=","verbose","display"],
    )
except Exception as e:
    print(str(e))

#! set defaults
filename = False
keyname = False
fromval = False
toval = False
verbose = False
display = False

for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-f", "--filename"): filename = arg
    if opt in ("-k", "--fmkey"): keyname = arg
    if opt in ("-F", "--fromval"): fromval = arg
    if opt in ("-T", "--toval"): toval= arg
    if opt in ("-v", "--verbose"): verbose = True
    if opt in ("-D", "--display"): display = True

#^ ---------------------------------------------------------------------------
#^ ---------------------------------------------------------------------------


# DIR="/home/jw/store/sites/tholonia/chirpy2/projects/videos"
fparts = split_path(filename)
DIR = fparts['dirname']
files = glob.glob(f"{DIR}/*md")

for file in files:
    print(file)
    with open(file) as f:
      post = frontmatter.load(f)
    show(post.metadata,Fore.GREEN)
    fmdata = get_key(keyname,post)
    if fmdata: #! kay exists
      if display:
        show(post.metadata[keyname],Fore.YELLOW)
      else:
        for fmd in fmdata:
          if fmd == fromval:  #! found key match
            snr_ary(fromval,toval,post.metadata[keyname])
        post.metadata[keyname] = list(filter(("86").__ne__, post.metadata[keyname]))
        show(post.metadata, Fore.CYAN)
        final = frontmatter.dumps(post)
        with open(file, 'w') as f:
          f.write(final)

