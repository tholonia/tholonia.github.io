#!/bin/env python

from pydub import AudioSegment


audio = AudioSegment.from_mp3("/tmp/ttx_en.mp3")
audio = audio.speedup(playback_speed=1.32)  # speed up by 2x
audio.export("/tmp/final.mp3", format="mp3")
