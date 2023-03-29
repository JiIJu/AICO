from threading import Thread
from pyaudio import PyAudio
from time import sleep
import wave

class Audio(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.wf = wave.open(f"./audio/hype.wav", 'rb')
        self.p = PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                            channels=self.wf.getnchannels(),
                            rate=self.wf.getframerate(),
                            output=True)
        self.daemon = True
        self._flag = False
        self.name = ""


    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, state):
        self._flag = state

    def start_audio(self, name):
        self.flag = True
        self.wf = wave.open(f"./audio/{name}.wav", 'rb')
    
    def stop_audio(self):
        self.flag = False

    def run(self):
        while 1:
            sleep(1)
            if not self._flag:
                continue
            print("sadsa")
            data = b"1"
            while self._flag and data:
                data = self.wf.readframes(1024)
                self.stream.write(data)
            self._flag = False

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        


if __name__ == "__main__":
    audio = Audio()

    audio.start()

    while(1):
        msg = int(input("hgellop"))
        if msg == 1:
            audio.start_audio("hype")
        elif msg == 2:
            audio.start_audio("nxde")
        else:
            audio.stop_audio()