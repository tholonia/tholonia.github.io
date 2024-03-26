#!/bin/env python
import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
from datetime import datetime
import yaml

init()

def ex(cmd):
  print(cmd)
  os.system(cmd)

def showhelp():
    print("help")
    rs = """
    -h, --help          show help
    -d, --date          YYYY-MM-DD
    -t, --title

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

    yaml_frontmatter = yaml.safe_load(''.join(yaml_lines))
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
      yaml.dump(yaml_frontmatter, file)
      file.write('---\n')

    # Write content
    file.write(content)


SITE_ROOT = "/home/jw/sites/tholonia/chirpy2"
POST_MD_ROOT = "/_posts"
POST_ASSET_ROOT = "/assets/posts"

verbose = False
image = f"{SITE_ROOT}/EX_post_image.jpg"
idate =  datetime.today().strftime('%Y-%m-%d')
title = "DElETE-ME"
full_title = False
src1 = False

# v ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# [ get args
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hd:t:i:s:",
        [
            "help",
            "date=",
            "title=",
            "image=",
            "src1=",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-i", "--image"):
        image = arg
    if opt in ("-t", "--title"):
        title = arg.replace(" ","-")

    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-d", "--date"):
        idate = arg
    if opt in ("-s", "--src1"):
        src1 = arg

full_title = f"{idate}-{title}"

print(Fore.CYAN + f"full_title:" + Fore.WHITE + full_title + Fore.RESET)

newfile = f"{SITE_ROOT}{POST_MD_ROOT}/{full_title}"
newpath = f"{SITE_ROOT}{POST_ASSET_ROOT}/{full_title}"
newimage = f"{POST_ASSET_ROOT}/{full_title}/post_image.jpg"

print(Fore.YELLOW + f"newfile:" + Fore.WHITE + newfile + Fore.RESET)
print(Fore.YELLOW + f"newpath:" + Fore.WHITE + newpath + Fore.RESET)
print(Fore.YELLOW + f"newimage:" + Fore.WHITE + newimage + Fore.RESET)


ex(f"cp {SITE_ROOT}/EX_post_template.md {newfile}.md")
ex(f"mkdir -p {newpath}")
ex(f"cp {image} {SITE_ROOT}/{newimage}")


post_yaml = read_yaml_frontmatter_and_content(f"{newfile}.md")

post_yaml['frontmatter']['date'] = idate
post_yaml['frontmatter']['title'] = title
post_yaml['frontmatter']['image'] = newimage

save_yaml_frontmatter_and_content(post_yaml, "test.md")

print(f"|{newfile}.md| ready")
