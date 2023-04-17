import os

class TTS:
    def speak(self, message, filename="audio.wav"):
        print("TTS: starting speaking")
        # generate audio file of text read out
        os.system("mimic3 \"" + message + "\" > " + filename)
        print("TTS: finished")

if __name__ == '__main__':
    tts = TTS()
    message = input("Enter the message to be spoken: ")
    tts.speak(message)
