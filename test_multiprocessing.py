#from multiprocessing import Process, Value, Array

import multiprocessing as mp
from ctypes import c_char_p
from time import sleep

def writer(a):
    sleep(1)
    #a[:] = ["up", "down", "left"]
    a[0] = b'Hallo'
def reader(a):
    sleep(0.1)
    print(str(a[0]))
    sleep(2)
    print(str(a[0], 'utf-8'))

if __name__ == '__main__':
    arr = mp.Array(c_char_p, 3)
    p = mp.Process(target=writer, args=(arr,))
    r = mp.Process(target=reader, args=(arr,))

    p.start()
    r.start()
    p.join()
    r.join()
