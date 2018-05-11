import RPi.GPIO as GPIO
import time
import threading

class InputPin(threading.Thread):
    
    def __init__(self,pin):
        threading.Thread.__init__(self)
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    
    def run(self):
        while(1):
            if GPIO.input(12) == 0:
                time.sleep(0.5)
                print("Input pin Works =[]! :D")
