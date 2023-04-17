import pyaudio
import wave
import audioop


class AudioRecorder:
    def __init__(self, threshold=500, low_time=2, high_time=0.2):
        self.threshold = threshold
        self.low_time = low_time
        self.high_time = high_time
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)

    def record(self, filename):
        print("Listening for recording")
        self.filename = filename
        self.is_recording = True
        self.frames = []
        low_count = 0
        high_count = 0
        # low phase
        while True:
            data = self.stream.read(1024)
            if len(self.frames) == self.high_time * 44100 // 1024:
                self.frames.pop(0)
            self.frames.append(data)
            rms = audioop.rms(data, 2)
            if rms > self.threshold:
                high_count += 1
                low_count = 0
            else:
                high_count = 0
                low_count += 1
            if high_count > self.high_time * 44100 // 1024:
                print("Start recording")
                break
        while True:
            data = self.stream.read(1024)
            self.frames.append(data)
            rms = audioop.rms(data, 2)
            if rms > self.threshold:
                low_count = 0
            else:
                low_count += 1
            if low_count > self.low_time * 44100 // 1024:
                print("Stop recording")
                self.is_recording = False
                break
        # save frames as wav file
        self.save()

    def save(self):
        wavefile = wave.open(self.filename, 'wb')
        wavefile.setnchannels(1)
        wavefile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(44100)
        wavefile.writeframes(b''.join(self.frames))
        wavefile.close()
        print(f"Recording saved as {self.filename}")

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.record("output.wav")
    recorder.record("output2.wav")
    recorder.close()
