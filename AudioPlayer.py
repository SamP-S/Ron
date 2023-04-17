import wave
import pyaudio
import time

class AudioPlayer:
    def __init__(self):
        self._pa = pyaudio.PyAudio()
        self._stream = None
        self._wavefile = None
    
    def play(self, filename):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
        if self._wavefile is not None:
            self._wavefile.close()
        
        self._wavefile = wave.open(filename, 'rb')
        self._stream = self._pa.open(
            format=self._pa.get_format_from_width(self._wavefile.getsampwidth()),
            channels=self._wavefile.getnchannels(),
            rate=self._wavefile.getframerate(),
            output=True
        )
        data = self._wavefile.readframes(1024)
        while data:
            self._stream.write(data)
            data = self._wavefile.readframes(1024)
        time.sleep(0.1)
        
    def close(self):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
        if self._wavefile is not None:
            self._wavefile.close()
        self._pa.terminate()

if __name__ == "__main__":
    player = AudioPlayer()
    player.play("hi.wav")
    player.play("bye.wav")
    player.close()