from threading import Thread, Event
from pyaudio import PyAudio
from time import sleep
import wave

import sounddevice as sd
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
        self.flag = False
        self.name = ""
        self.event = Event()


    def audio_start(self, name):
        self.flag = True
        self.wf = wave.open(f"./audio/{name}.wav", 'rb')
        self.event.set()
        print(f"Audio Start >> {name}")
    
    def audio_stop(self):
        self.flag = False

    def run(self):
        while 1:
            self.event.wait()
            self.event.clear()

            data = b"1"
            while self.flag and data:
                data = self.wf.readframes(1024)
                self.stream.write(data)
            self.flag = False


        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        


if __name__ == "__main__":
    from voice import Voice
    eventVoice = Event()
    voice = Voice(eventVoice)

    audio = Audio()
    audio.start()
    states = ["그만해", "노래 꺼줘", "뮤직 스타트", "배경 소음", "시작해", "운동 시작", "운동 종료", "음악 틀어", "하이 아이코"]
   
    with sd.InputStream(
                channels=1,
                samplerate=44032,
                blocksize=22016,
                latency=0.0,
                callback=voice.sd_callback):
        while(1):
            print("Command Wait...")
            eventVoice.wait()
            eventVoice.clear()
            msg = voice.command
            print(f"Command >> '{states[msg]}'")
            sleep(1)
            if msg == 1:
                audio.start_audio("hype")
            elif msg == 2:
                audio.start_audio("nxde")
            elif msg == 3:
                audio.start_audio("pu")
            elif msg == 4:
                audio.start_audio("sq") 
            else:
                audio.stop_audio()