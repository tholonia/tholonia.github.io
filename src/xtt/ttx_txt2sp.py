#!/bin/env python

from gtts import gTTS

import os
with open("/tmp/ttx_en.txt") as f:
  text =f.read()

# Create a gTTS object
tts = gTTS(text,lang="en-us",tld="us", slow=False)

# Save the generated speech to a file
tts.save("/tmp/ttx_en.mp3")
