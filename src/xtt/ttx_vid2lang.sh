#!/bin/bash

V="https://www.youtube.com/watch?v=JUVsIDwZ5WI"

#$grab Video
ytgrab  ${V} ttx_vid

#etract audio
ffmpeg -y -loglevel warning -i  ~/Videos/ttx_vid.mp4 -vn -ar 44100 -ac 2 -ab 192k -f mp3 /tmp/ttx_audio.mp3

#transcribe
#https://github.com/openai/whisper
whisper /tmp/ttx_audio.mp3 \
  --model large \
  --language Spanish \
  --task translate \
  |awk -F "]" '{print $2}'> /tmp/ttx_en.txt

# text 2 speech
#https://gtts.readthedocs.io/en/latest/
./ttx_txt2sp.py

# bump speed by 15%
./ttx_speedup.py

#replace audio
ffmpeg -y -loglevel warning -i ~/Videos/ttx_vid.mp4 -i /tmp/final.mp3 -c:v copy -map 0:v:0 -map 1:a:0 ttx_en.mp4

echo "FINAL: `pwd`/ttx_en.mp4"

