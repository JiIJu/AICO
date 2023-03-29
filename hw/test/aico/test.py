from threading import Thread
import sounddevice as sd
import numpy as np
import tensorflow as tf
from test_audio import Audio
# Parameters
sample_rate = 44032
blocksize = 22016
model_path = "C:\\Users\\SSAFY\\Desktop\\socket\\aico\\5soundclassifier_with_metadata.tflite"
#model_path = "C:\\Users\\SSAFY\\Desktop\\socket\\aico\\wake_word_stop_lite.tflite"


# Load model (interpreter)
interpreter = tf.lite.Interpreter(model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)
print(output_details)

buffer = np.zeros(sample_rate, dtype=np.float32)
print("hehe", len(buffer))

def sd_callback(rec, frames, time, status):
    global buffer
    buffer = buffer[blocksize:]
    buffer = np.append(buffer, np.float32(rec.reshape(frames)))
    #print(buffer)
    # print(len(buffer))
    # print(buffer)
    # print(len(buffer))
    # print(buffer)
    # Start timing for testing
    #start = timeit.default_timer()
    
    # Notify if errors
    if status:
        print('Error:', status)
    
    # Remove 2nd dimension from recording sample
    #rec = np.squeeze(rec)

    # Resample
    # rec, new_fs = decimate(rec, sample_rate, resample_rate)
    # print("fs")
    # print(new_fs)
    # Save recording onto sliding window
    # window[:len(window)//2] = window[len(window)//2:]
    # window[len(window)//2:] = rec
    
    
    # # # Compute features
    # mfccs = python_speech_features.base.mfcc(rec, 
    #                                     samplerate=44032,
    #                                     winlen=1,
    #                                     winstep=0.1,
    #                                     numcep=num_mfcc,
    #                                     nfilt=26,
    #                                     nfft=2048,
    #                                     preemph=0.0,
    #                                     ceplifter=0,
    #                                     appendEnergy=False,
    #                                     winfunc=np.hanning)
    # # mfccs = mfccs.transpose()
    # print(np.shape(mfccs))
    # Make prediction from model

    in_tensor = np.float32(buffer.reshape(1 , sample_rate))
    interpreter.set_tensor(input_details[0]['index'], in_tensor)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    output = output_data[0]

    # 0 그만해
    # 1 노래 꺼줘
    # 2 뮤직 스타트
    # 3 배경 소음
    # 4 시작해
    # 5 운동 시작
    # 6 운동 종료
    # 7 음악 틀어
    # 8 하이 아이코
    state = ["그만해", "노래꺼줘", "뮤직 스타트", "배경 소음", "시작해", "운동 시작", "운동 종료", "음악 틀어", "하이 아이코"]
    #그만해, 노래꺼조, 뮤지익 스타트, 시자케, 운동 시작, 운동 종뇨, 으막 트러, 하이 아이코
    maxi = max(output)
    if maxi < 0.5:
        print("nothing")
        return
    print(f"{state[output.argmax()]} >> {maxi:.2f}")
    
    x =  [f"{o:.2f}" for o in output]
    print(x)
    #end = timeit.default_timer()
    #print("time diff >> ", end - start)

from time import sleep

# Start streaming from microphone
with sd.InputStream(channels=1,
                    samplerate=sample_rate,
                    blocksize=blocksize,
                    #blocksize=sample_rate,
                    latency=0.0,
                    callback=sd_callback):
    while True:
        sleep(1000)

