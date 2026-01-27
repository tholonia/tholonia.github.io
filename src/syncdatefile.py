#!/bin/env python
import glob
from datetime import datetime, timedelta
import frontmatter
import os
from pprint import pprint
import getopt,sys

def showhelp():
    print("help")
    rs = """
    -h, --help          show help
    -f, --filename      filename
    -o, --outerpri date pri
    -i, --innerpri date pri
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

# v ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# [ get args
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hf:io",
        [
            "help",
            "ilename=",
            "innerpri",
            "outerpri",
        ],
    )
except Exception as e:
    print(str(e))

filename = False
innerpri = False
outerpri = False

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-f", "--filename"):
      filename = arg
    if opt in ("-i", "--innerpri"):
      innerpri = True
    if opt in ("-o", "--outerpri"):
      outerpri = True



DIR="/home/jw/store/sites/tholonia/chirpy2/projects/videos"
format_str = '%Y-%m-%d'
fparts = split_path(filename)
parts = fparts['basename'].split("_",1)
outer_date_str = parts[0]
fn_append = parts[1]

with open(filename) as f:
  post = frontmatter.load(f)
inner_date_str = post.metadata['date']


# print(f"inner: [{inner_date_str}]")
# print(f"outer: [{outer_date_str}]")
if inner_date_str == outer_date_str:
  print("Dates in sync")
else:
  if innerpri == True:
    print(f"Setting outer date to inner date {inner_date_str}")
  if outerpri == True:
    print(f"Setting inner date to outer date {outer_date_str}")
    post.metadata['date']=outer_date_str
    final = frontmatter.dumps(post)
    with open(filename, 'w') as f:
      f.write(final)





    # newfilename = f"{}_{fn_append}"
    # with open(newfilename, 'w') as f:
    #   f.write(final)
    # os.unlink(filename)


#
#
# newdatestr = "{:%Y-%m-%d}".format(new_datetime_obj)
# newfilename = f"{fparts['dirname']}/{newdatestr}-{parts[1]}"
# print(f"newfile: {newfilename}")
# # print("NEW",new_datetime_obj.date())
#
# final = frontmatter.dumps(post)
# # pprint(post.metadata['tags'])    final = frontmatter.dumps(post)
# # pprint(final)
# with open(newfilename, 'w') as f:
#   f.write(final)
# os.unlink(filename)
#
