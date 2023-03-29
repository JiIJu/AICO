from threading import Thread
from time import sleep
from queue import Queue

from client import Communication

from voice import Voice


if __name__ == "__main__":

    queueVoice = Queue()

    voice = Voice(queueVoice)


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

    enable = True
    enable2 = False
    while 1:
        print("Command Wait...")
        command = queueVoice.get()
        print(f"Command >> {states[command]}")
        
        if command == 2 or command == 7:
            print("222222_777777")
            continue
        if command == 1:
            print("11111111111111")
            continue

        if command == 8 and enable:
            print("8888888888888")
            enable = False
            continue

        if command == 4 or command == 5:
            # 서버와 연결
            print("44444_555555")
            continue;

        if command == 6 or command == 0:
            print("66666")
            enable = True
            continue

        if enable:
            continue

# hw
# FV87F5NJXooLALKmD6X4