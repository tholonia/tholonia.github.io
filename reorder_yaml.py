#!/bin/env python

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
from datetime import datetime
import oyaml
from time import time

init()

def ex(cmd):
  print(cmd)
  os.system(cmd)


def showhelp():
    print("help")
    rs = f"""
    Usage: {__file__} [OPTION]...
    Reorder the YAML data in a md file

    -h, --help
    -f, --filename
    -x, --execute      Without -x, runs in dryrun mode

"""
    print(rs)
    exit()

def read_yaml_frontmatter_and_content(file_path):
  with open(file_path, 'r') as file:
    lines = file.readlines()

  # Check if the file contains YAML frontmatter
  if lines[0].strip() == '---':
    yaml_lines = []
    i = 1
    # Extract YAML lines until the end of frontmatter
    while lines[i].strip() != '---':
      yaml_lines.append(lines[i])
      i += 1

    yaml_frontmatter = oyaml.safe_load(''.join(yaml_lines))
    content = ''.join(lines[i + 1:])
  else:
    # If no frontmatter, assume content starts from the beginning
    yaml_frontmatter = {}
    content = ''.join(lines)

  return {'frontmatter': yaml_frontmatter, 'content': content}

def save_yaml_frontmatter_and_content(data_dict, file_path):
  yaml_frontmatter = data_dict['frontmatter']
  content = data_dict['content']

  with open(file_path, 'w') as file:
    if yaml_frontmatter:
      # Write YAML frontmatter
      file.write('---\n')
      oyaml.dump(yaml_frontmatter, file,sort_keys=False)
      file.write('---\n')

    # Write content
    file.write(content)



# v ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# [ get args
execute = False
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hf:x",
        [
            "help",
            "filename="
            "execute"
        ],
    )
except Exception as e:
    print(str(e))



SITE_ROOT="/home/jw/store/sites/tholonia/chirpy2"
filename = False #f"{SITE_ROOT}/_material/book_red_NOTFREE.md"
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-f", "--filename"): filename = arg
    if opt in ("-x", "--execute"): execute = True

order = [
  'layout',
  'title',
  'author',
  'date',
  'image',
  'categories',
  'source1',
  # 'src1',
  # 'src1_title',
  'ptags',
  'jday',
  'tags',
  'purchase',
]

#! first make a backup
nd = f"/tmp/mdbackup_{int(time()/60)}" #get minutes
if os.path.isdir(nd):
  pass
else:
  os.system(f"mkdir {nd}")

os.system(f"cp {filename} {nd}")

print(f"reordering: {Fore.GREEN}{filename}{Fore.RESET}")


# ptags: [nokwgen-manual]



post = read_yaml_frontmatter_and_content(filename)
#! fix the YAML by combinign existing src1 and src1_title to be elements of 'source1'
# if not "source1" in post['frontmatter']:
#   if "src1" in post['frontmatter']:
#     source1 = {'src':post['frontmatter']['src1'],'title':post['frontmatter']['src1_title']}
#     del post['frontmatter']['src1']
#     del post['frontmatter']['src1_title']
#   else:
#     source1=post['frontmatter']['source1']
#   post['frontmatter']['source1']=source1

# pprint(post)
with open("/tmp/newfm.md","w") as f:
  f.write("---\n")
  for k in order:
    try:
      f.write(f"{k}: {post['frontmatter'][k]}\n")
    except:
      print(f"Skipping:{Fore.RED}{k}{Fore.RESET}")
  f.write("---\n")
  f.write(post['content']+"\n")

#! now reread teh ordered yaml
post = read_yaml_frontmatter_and_content("/tmp/newfm.md")
#! and have yaml rewroite ot in teh proper format
if execute:
  print(f"WRITING:{Fore.LIGHTWHITE_EX}{filename}{Fore.RESET}")
  save_yaml_frontmatter_and_content(post, filename)

#
