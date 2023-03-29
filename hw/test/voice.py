from threading import Thread
import sounddevice as sd
import numpy as np
import tensorflow as tf

class Voice(Thread):
    def __init__(self, queue):
        Thread.__init__(self)

        # Load model (interpreter)
        self.interpreter = tf.lite.interpreter("../test_data/5soundclassifier_with_metadata.tflite")
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.buffer = np.zeros(44032, dtype=np.float32)
        self.queue = queue
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

        if max(output) < 0.5:
            return
        
        # x =  [f"{o:.2f}" for o in self.output]
        # print(x)
        #end = timeit.default_timer()
        #print("time diff >> ", end - start)

        self.queue.put(index)



    def run(self):
        with sd.InputStream(
                        channels=1,
                        samplerate=44032,
                        blocksize=22016,
                        latency=0.0,
                        callback=self.sd_callback):
            while 1:
                pass

if __name__ == "__main__":
    from queue import Queue

    queue = Queue()
    voice = Voice(queue)
    voice.start()