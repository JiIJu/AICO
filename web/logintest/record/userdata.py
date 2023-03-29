

class Userdata(object):
    def __init__(self):
        self.time = 0
        self.check = 1
        return

globals()['time_{}'.format(1)] = Userdata()
globals()['time_{}'.format(1)].time = 42


i=1

if 'time_{}'.format(i) in globals():
    print('하이')