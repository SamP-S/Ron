import speech_recognition as sr
from os import path

class Transcriber:

    ERROR_FLAG = "ERROR"

    # setup transcriber
    def __init__(self, filename="audio.wav"):
        self.AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)
        self.recogniser = sr.Recognizer()
        
    def transcribe(self):
        # read the entire audio file
        with sr.AudioFile(self.AUDIO_FILE) as source:
            audio = self.recogniser.record(source)
        # recognize speech using Google Speech Recognition
        try:
            text = self.recogniser.recognize_google(audio)
            print("Google Speech Recognition: \"" + text + "\"")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return self.ERROR_FLAG
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return self.ERROR_FLAG
        return text
        
if __name__ == "__main__":
    scribe = Transcriber()
    scribe.transcribe()
