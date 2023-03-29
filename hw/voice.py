from pycoral.utils.edgetpu import make_interpreter
import numpy as np

class Voice():
    def __init__(self, event):

        # Load model (interpreter)
        self.interpreter = make_interpreter("../test_data/7soundclassifier_with_metadata.tflite")
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.buffer = np.zeros(44032, dtype=np.float32)
        self.event = event
        self.command = -1
        self.daemon = True

        print(self.input_details)
        print(self.output_details)

    def sd_callback(self, rec, frames, time, status):
        self.buffer = self.buffer[frames:]
        self.buffer = np.append(self.buffer, np.float32(rec.reshape(frames)))
        
        # Notify if errors
        if status:
            print('Error:', status)
        

        in_tensor = np.float32(self.buffer.reshape(1 , 44032))
        self.interpreter.set_tensor(self.input_details[0]['index'], in_tensor)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        output = output_data[0]


        index = output.argmax()
        if index == 3:
            return
        print(f"Voice >> {index}, {max(output)}")
        if max(output) < 0.5:
            return
        
        # x =  [f"{o:.2f}" for o in self.output]
        # print(x)
        #end = timeit.default_timer()
        #print("time diff >> ", end - start)
        self.event.set()
        self.command = index

if __name__ == "__main__":
    from threading import Thread, Event
    from time import sleep
    import sounddevice as sd

    eventVoice = Event()
    voice = Voice(eventVoice)

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

    with sd.InputStream(
                channels=1,
                samplerate=44032,
                blocksize=22016,
                latency=0.0,
                callback=voice.sd_callback):
        while 1:
            print("Command Wait...")
            eventVoice.wait()
            eventVoice.clear()
            command = voice.command
            print(f"Command >> '{states[command]}'")
            sleep(1)