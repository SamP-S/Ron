from GoogleTranscriber import *
from RonGPT import *
from TTS import *
from VoskLiveTranscriber import *
from AudioRecorder import *
from AudioPlayer import *
import os

liveScribe = LiveTranscriber()
scribe = Transcriber("audio.wav")
ron = Ron()
tts = TTS()
recorder = AudioRecorder()
player = AudioPlayer()

liveScribe.start_transcribing()
player.play("audio/hi.wav")

while True:
    recorder.record("audio.wav")
    user_text = scribe.transcribe()
    if "stop" in user_text:
        print("OK: stopping")
        break
    if user_text == scribe.ERROR_FLAG:
        print("Error: Transcriber failed, try again")
    else:
        ron_text = ron.send_gpt(user_text)
        print(ron_text)
        tts.speak(ron_text, "audio.wav")
        player.play("audio.wav")

recorder.close()
player.play("audio/bye.wav")
print("finished")