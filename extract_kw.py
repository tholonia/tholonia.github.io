#!/bin/env python
"""
alias KW="~/src/KeyBERT/extract_kw.py -f "
KW assets/material/chinese_rainmaking.pdf
"""
from keybert import KeyBERT
from tika import parser # pip install tika

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
init()

def showhelp():
    print("help")
    rs = """
    -h, --help          show help
    -f, --filename      filename
    -D, --directory
    -d, --debug
"""
    print(rs)
    exit()


# [set default vals
verbose = False
filename = False
directory = False
# v ────────────────────────────────────────────────────────────────────────────────────────────────────────────
# [ get args
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hf:dD:",
        [
            "help",
            "filename=",
            "debug",
            "directory="
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-f", "--filename"):
        filename = arg
    if opt in ("-d", "--debug"):
        verbose = True
    if opt in ("-D", "--directory"):
        directory = arg

if filename == False and directory == False:
    showhelp()

def getContent(fn):
    print(Fore.WHITE+f"{fn}"+Fore.RESET)
    # raw = parser.from_file('/home/jw/store/sites/tholonia/chirpy2/assets/material/Introduction_to_Complex_Systems_Sustainability_and.pdf')
    raw = parser.from_file(fn)
    doc = raw['content']

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(doc)
    # keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), stop_words=None)
    # keywords = kw_model.extract_keywords(doc, highlight=True)
    str = "["
    for kw in keywords:
        print(Fore.YELLOW + f"{kw[0]}", Fore.GREEN + f"{kw[1]}" + Fore.RESET)
        str += kw[0] + ","
    str = str.strip(",") + "]"

    print(Fore.CYAN + str + Fore.RESET)

if directory != False:
    files = glob.glob(f"{directory}/*.pdf")
    for file in files:
        getContent(file)
else:
    getContent(filename)

