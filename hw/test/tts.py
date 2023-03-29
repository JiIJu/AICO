import gtts
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
        self.wf = wave.open(f"./{name}", 'rb')
    
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
    import gtts
    import pygame
    
    text = "너 같은 멍청한 인간은 처음 본다. 휴먼"
    tts = gtts.gTTS(text, lang='ko')
    tts.save("hello.mp3")


    import pygame

    music_file = "hello.mp3"   # mp3 or mid file


    freq = 16000    # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
    bitsize = -16   # signed 16 bit. support 8,-8,16,-16
    channels = 1    # 1 is mono, 2 is stereo
    buffer = 2048   # number of samples (experiment to get right sound)

    # default : pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(30)
    pygame.mixer.quit()   