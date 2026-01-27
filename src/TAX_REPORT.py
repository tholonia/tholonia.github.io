#!/bin/env python
"""
Read PDF file, limit to 10 srcwords, outpout in FM format
./CATWORD.py -f assets/material/chinese_rainmaking.pdf  -l 10 -s 2

"""
import toml
import sys, getopt
from colorama import init, Fore, Back
init()


def showhelp():
  print("help")
  rs = """
    -h, --help          show help
"""
  print(rs)
  exit()

#^ ---------------------------------------------------------------------------
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "ht:",
        ["help","taxonomy="],
    )
except Exception as e:
    print(str(e))

#! set defaults
report = False
taxonomy = "relevant"
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-t", "--taxonomy"): taxonomy = arg


#^ ---------------------------------------------------------------------------

# with open("taxonomy2.toml", mode="rb") as fp:
config = toml.load("taxonomy2.toml")
space = "         "
# print(config)
border = f"""
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   STARTING:   {space:96s}│
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""
print(Fore.CYAN+border+Fore.RESET)
#! report count for each catagory
for cat in config[taxonomy]:
  print(f"{cat:20s}: {len(config[taxonomy][cat])}")

