from threading import Thread, Event
from time import sleep
from queue import Queue

from motor import Motor
from videoUDP import Video
from client import Communication
from voice import Voice
from audio import Audio
import sounddevice as sd


if __name__ == "__main__":
    eventCommu = Event()
    eventVideo = Event()
    eventMotor = Event()
    eventVoice = Event()

    # socket 통신
    communication = Communication(("192.168.100.106", 10000), eventCommu)
    communication.start()
    sleep(0.5)
    # 객체 생성
    audio = Audio()
    motor = Motor(eventMotor)
    voice = Voice(eventVoice)
    video = Video(("192.168.100.106", 10050), eventVideo)
    video.start()
    sleep(0.5)
    audio.start()
    audio.audio_start("open")
    
    print("서버에 접속 중...")
    eventCommu.wait()
    eventCommu.clear()
    print("접속 완료!")

    motor.pose = video.msg
    motor.start()

    # 0 그만해
    # 1 노래 꺼줘
    # 2 뮤직 스타트
    # 3 배경 소음
    # 4 시작해
    # 5 운동 시작
    # 6 운동 종료
    # 7 음악 틀어
    # 8 하이 아이코

    states = ["그만해", "노래 꺼줘", "뮤직 스타트", "배경 소음", "시작해", "운동 시작", "운동 종료", "음악 틀어", "하이 아이코"]
    # 그만해, 노래꺼조, 뮤지익 스타트, 시자케, 운동 시작, 운동 종뇨, 으막 트러, 하이 아이코

    modes = [1, 0]
    enable = True
    with sd.InputStream(
                channels=1,
                samplerate=44032,
                blocksize=22016,
                latency=0.0,
                callback=voice.sd_callback):
        while 1:
            print("Command Wait...")
            eventVoice.wait()
            sleep(1)
            eventVoice.clear()
            command = voice.command
            # command = int(input("입력"))
            print(f"Command >> '{states[command]}'")
            
            if command == 2 or command == 7:
                audio.audio_start("hype")
                continue

            if command == 1:
                audio.audio_stop()
                continue

            if command == 6:
                audio.audio_start("correct")
                video.stop_video()
                enable = True
                communication.send("stop")
                continue

            if command == 8 and enable:
                # 초기화
                print("위치 조정 중...")
                audio.audio_stop()
                video.stop_video()
                communication.send("go")

                # 위치 조정 [1, 0]
                motor.modes = modes
                video.modes = modes
                eventMotor.set()
                eventVideo.set()
                sleep(2)

                # 위치 조정 끝나면
                eventMotor.wait()
                eventMotor.clear()
                audio.audio_start("sq")
                video.stop_video()
                print("위치 조정이 끝났습니다!")
                communication.send("start")
                sleep(1)

                # video init 종료
                eventVideo.set()         
                enable = False
                continue
            if (command == 4 or command == 5) and enable:
                # 초기화
                print("위치 조정 중...")
                audio.audio_stop()
                video.stop_video()
                communication.send("go")

                # 위치 조정
                motor.modes = [1, 1]
                video.modes = [1, 1]
                eventMotor.set()
                eventVideo.set()
                sleep(3)

                # 위치 조정 끝나면 카메라 전환
                eventMotor.wait()
                eventMotor.clear()
                audio.audio_start("pu")
                eventMotor.wait()
                eventMotor.clear()
                audio.audio_start("correct")
                communication.send("start")
                video.stop_video()
                print("위치 조정이 끝났습니다!")
                sleep(1)

                # video init 종료
                eventVideo.set()         
                enable = False
                continue

