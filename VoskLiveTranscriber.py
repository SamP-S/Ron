import argparse
import queue
import sys
import sounddevice as sd

from vosk import Model, KaldiRecognizer

class LiveTranscriber:
    def __init__(self, filename=None, device=None, samplerate=None, model_lang="en-us"):
        self.filename = filename
        self.device = device
        self.samplerate = samplerate
        self.model_lang = model_lang
        self.q = queue.Queue()
        self.rec = None
        self.dump_fn = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def start_transcribing(self):
        try:
            if self.samplerate is None:
                device_info = sd.query_devices(self.device, "input")
                self.samplerate = int(device_info["default_samplerate"])
                
            self.model = Model(lang=self.model_lang)
            
            if self.filename:
                self.dump_fn = open(self.filename, "wb")
            else:
                self.dump_fn = None

            with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=self.device,
                    dtype="int16", channels=1, callback=self._callback):
                print("#" * 80)
                print("Press Ctrl+C to stop the recording")
                print("#" * 80)

                self.rec = KaldiRecognizer(self.model, self.samplerate)
                while True:
                    data = self.q.get()
                    if self.rec.AcceptWaveform(data):
                        text = self.rec.Result()
                        print(text)
                        if "ron" in text:
                            print("RON DETECTED")
                            return
                    else:
                        print(self.rec.PartialResult())
                    if self.dump_fn is not None:
                        self.dump_fn.write(data)

        except KeyboardInterrupt:
            print("\nDone")
        except Exception as e:
            print(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    transcriber = VoskTranscriber(filename="output.wav", device=1, model_lang="en-us")
    transcriber.start_transcribing()