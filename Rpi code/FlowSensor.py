import serial
import time
import threading

class Measure(threading.Thread):
    
    def run(self):
        ser = serial.Serial('/dev/ttyACM0', 9600)
        switch = 0
        while(1):
            time.sleep(3)
            msg = ser.readline()
            new = (msg.decode('utf-8'))
            new2 = int(new)
            print(new2)
            ser.flushInput()
            if(new2 == 100000):
                switch = 0
            if(new2 < 99000 and switch == 0):
                print("Haal 1 vat van voorraad af.")
                switch = 1