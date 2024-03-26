#!/bin/env python
import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
from datetime import datetime

init()

def ex(cmd):
  print(cmd)
  os.system(cmd)

def days_from_date_to_now(year, month, day):
  # Create a datetime object for the arbitrary date
  arbitrary_date = datetime(year, month, day)

  # Get the current date
  current_date = datetime.now()

  # Calculate the difference in days
  delta = current_date - arbitrary_date

  # Extract the days from the delta
  return delta.days

def showhelp():
    print("help")
    rs = """
    -h, --help          show help
    -d, --date          YYYY-MM-DD
    -t, --title
    -i, --image
    -s, --src1
    -S, --src1title

"""
    print(rs)
    exit()



import yaml


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


arbitrary_year = 2000
arbitrary_month = 1
arbitrary_day = 1

SITE_ROOT = "/home/jw/sites/tholonia/chirpy2"
MATERIAL_MD_ROOT = "/_material"
MATERIAL_ASSET_ROOT = "/material/assets"
MATERIAL_ASSET_WROOT = "/_material/assets"

verbose = False
image = f"{SITE_ROOT}/EX_post_image.jpg"
idate =  datetime.today().strftime('%Y-%m-%d')
title = "DElETE-ME"
full_title = False
src1 = False
src1title = False

# v ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# [ get args
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hd:t:i:s:S:",
        [
            "help",
            "date=",
            "title=",
            "image=",
            "src1=",
            "src1title=",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-i", "--image"):
        image = arg
    if opt in ("-t", "--title"):
        title = arg
        ntitle = title.replace(" ", "-").lower()
        # atitle = title.replace(" ", "_").lower()

    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-d", "--date"):
        idate = arg
    if opt in ("-s", "--src1"):
        src1 = arg
    if opt in ("-S", "--src1title"):
        src1title = arg

#^ the pattern for both MD and IMG is: "material"|"book"|etc followierd by a "_"
#^ filenames are all lowercased, and spaces replaces ith "-"


full_ntitle = f"material_{ntitle}"

print(Fore.CYAN + f"full_title:" + Fore.WHITE + full_ntitle + Fore.RESET)

newfile = f"{SITE_ROOT}{MATERIAL_MD_ROOT}/{full_ntitle}"
newpath = f"{SITE_ROOT}{MATERIAL_ASSET_ROOT}/{full_ntitle}"
newimage = f"{MATERIAL_ASSET_ROOT}/material_{ntitle}.jpg" #! this point to teh live location
newimage_cp = f"{MATERIAL_ASSET_WROOT}/material_{ntitle}.jpg" #! need to point to the working dir, not the live location

print(Fore.YELLOW + f"newfile:" + Fore.WHITE + newfile + Fore.RESET)
print(Fore.YELLOW + f"newpath:" + Fore.WHITE + newpath + Fore.RESET)
print(Fore.YELLOW + f"newimage:" + Fore.WHITE + newimage + Fore.RESET)

ex(f"cp {image} {SITE_ROOT}{newimage_cp}")

post_yaml = read_yaml_frontmatter_and_content(f"{SITE_ROOT}/EX_material_template.md")

post_yaml['frontmatter']['date'] = idate
post_yaml['frontmatter']['title'] = title
post_yaml['frontmatter']['image'] = newimage
post_yaml['frontmatter']['jday'] = days_from_date_to_now(arbitrary_year, arbitrary_month, arbitrary_day)

pprint(post_yaml)

if src1 != False:
  post_yaml['frontmatter']['src1'] = src1
  post_yaml['frontmatter']['src1_title'] = src1title


save_yaml_frontmatter_and_content(post_yaml, f"{newfile}.md")
print(f"|{newfile}.md| ready")

# save_yaml_frontmatter_and_content(post_yaml, f"test.md")
# print(f"|test.md| ready")
