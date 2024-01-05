#!/bin/env python

import sys

oneline = ""
for line in sys.stdin:
    oneline += " "+line.rstrip()

oneline.replace("\"","")
olary = oneline.split()
olary = list(set(olary))
olary = sorted(olary)

cats = [
   'ASTRONOMY',
   'BIOSCIENCE',
   'COMMUNICATION',
   'ECONOMICS',
   'ENERGY',
   'ESOTERIC',
   'GEOMETRY',
   'GEOSCIENCE',
   'HEALTH',
   'MATH',
   'METAPHYSICS',
   'NATURE',
   'NEUROSCIENCE',
   'PARAPSYCHOLOGY',
   'PHILOSOPHY',
   'PHYSICS',
   'POLITICS',
   'PSYCHOLOGY',
   'REFERENCE',
   'STRUCTURE',
   'TECHNOLOGY'
 ]

rary = []
for w in olary:
  if w in cats:
    rary.append(w)

print("["+",".join(rary)+"]")

