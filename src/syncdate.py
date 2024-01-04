#!/bin/env python
import glob
from datetime import datetime, timedelta
import frontmatter
import os
from pprint import pprint


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


DIR="/home/jw/store/sites/tholonia/chirpy2/projects/videos"
newtime = "2020-01-01"
format_str = '%Y-%m-%d'
files = glob.glob(f"{DIR}/*md")
new_datetime_obj = datetime.strptime(newtime, format_str)
for file in files:
    fparts = split_path(file)
    parts = fparts['basename'].split("_",1)
    date_str = parts[0]
    fname = parts[1]
    old_datetime_obj = datetime.strptime(date_str, format_str)
    new_datetime_obj = new_datetime_obj+timedelta(days=10)
    newdatestr = "{:%Y-%m-%d}".format(new_datetime_obj)
    newfilename = f"{fparts['dirname']}/{newdatestr}-{parts[1]}"
    print(f"newfile: {newfilename}")
    # print("NEW",new_datetime_obj.date())

    with open(file) as f:
      post = frontmatter.load(f)
    post.metadata['date'] = f"{new_datetime_obj.date()}"
    final = frontmatter.dumps(post)
    # pprint(post.metadata['tags'])    final = frontmatter.dumps(post)
    # pprint(final)
    with open(newfilename, 'w') as f:
      f.write(final)
    os.unlink(file)



    # with open(f"{DIR}/'tests/yaml/hello-world.txt') as f:

