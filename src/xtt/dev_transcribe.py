#!/bin/env python
"""
Options:
    -h, --help          show help
    -b, --base
    -s, --source        filename
    -v, --verbose       default: OFF
"""
import sys, getopt, os
from pprint import pprint
import subprocess
import whisper
#! for ASNI colors outout
import lib_ollama as lo

from colorama import init, Fore, Back
init()


def showhelp():
  print("help")
  rs = """
    -h, --help          show help
    -b, --base          model
    -s, --source        filename ro URL or source
    -v, --verbose       default: OFF
    -F, --fromlang      default: Spanish
    -T, --tolang        default: English
"""
  print(rs)
  exit()

#! ---------------------------------------------------------------------------
#! Set default values
source = False
verbose = False
speak = False
base = "medium"
fromlang = "Spanish"
tolkang = "English"
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hb:s:vS:F:T:",["help","base=","source=","verbose","speak","fromlang","tolang"])
except Exception as e:
    print(str(e))

#! set defaults
for opt, arg in opts:
    if opt in ("-h", "--help"): showhelp()
    if opt in ("-b", "--base"): base = arg
    if opt in ("-s", "--source"): source = arg
    if opt in ("-v", "--verbose"): verbose = True
    if opt in ("-S", "--speak"): speak = True
    if opt in ("-F", "--fromlang"): fromlang = arg
    if opt in ("-T", "--tolang"): tolang = arg

#^ ---------------------------------------------------------------------------
print(Fore.YELLOW+source+Fore.RESET)

model = whisper.load_model(base)
result = model.transcribe(source)

print("────────────────────────────────────────────────────────────────────")
print(Fore.CYAN+result['text'])
if speak:
  with open("/tmp/olammatmp","w") as f:
    f.write(result['text'])
  rs = lo.prunlive(f"/bin/mimic -f /tmp/olammatmp",debug=verbose)
print(rs)
print("────────────────────────────────────────────────────────────────────")
