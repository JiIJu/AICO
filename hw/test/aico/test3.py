import speech_recognition as sr

import sys
import librosa
import sklearn
import os
from scipy.io import wavfile
from collections import defaultdict, Counter
from scipy import signal

import tensorflow as tf
import numpy as np

from keras.layers import Dense
from keras import Input, Model
from keras.models import load_model
from keras.utils import to_categorical
from keras.layers import Dense
from pydub import AudioSegment

ans_label = ['turn_off', 'turn_on', 'noise', 'start', 'end', 'hello']
r = sr.Recognizer()
ans = 0

with sr.Microphone() as source:
    print("Say order")
    speech = r.listen(source)

with open("audio_file.wav", "wb") as file:
    file.write(speech.get_wav_data())

try : 
    interpreter =  tf.lite.Interpreter(model_path = "C:\\Users\\multicampus\\S08P12C102-1\\S08P12C102-10\\ai\\soundclassifier_with_metadata.tflite")
    interpreter.allocate_tensors()

    input = interpreter.get_input_details()
    output = interpreter.get_output_details()

    audio, sr = librosa.load("C:\\Users\\multicampus\\Desktop\\we\\audio_file.wav" , sr=16000)
        
    mfcc = librosa.feature.mfcc(audio, sr=16000, n_mfcc=124, n_fft= 10, hop_length = 160)
    mfcc = sklearn.preprocessing.scale(mfcc, axis = 1)
    pad2d=lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a.shape[0], i-a.shape[1]))
    padded_mfcc = pad2d(mfcc, 129)
    padded_mfcc = np.expand_dims(padded_mfcc, (0,3))

    for inp in input:
        input_data = np.array(np.random.random_sample(inp['shape']), dtype=np.float32)
        interpreter.set_tensor(inp['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output[0]['index'])
    print(*output_data)
    print(padded_mfcc.shape)
    print(output_data )
except sr.UnknownValueError:
    print("your speech can not understand")
except sr.RequestError as e:
    print("Request Error! {0}".format(e))