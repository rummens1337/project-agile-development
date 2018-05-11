import sys
from threading import Thread
sys.path.append("/home/pi/PAD/Python/MFRC522-python")
import Nfc
sys.path.append("/home/pi/PAD/Python/HX711")
import Weigh
import time
import Test
import FlowSensor

    
def main():
    # initialize threads
    reader = Nfc.Read()
    hx711 = Weigh.Scale()
    beer_o_meter = FlowSensor.Measure()
    #pin1 = Test.InputPin("12")
    
    # start threads. these now run seperately.
    reader.start()
    hx711.start()
    beer_o_meter.start()
    #pin1.start()
    
    while True:
        try:
            time.sleep(2)
            print("Main program still running...")
            
        except(KeyboardInterrupt, SystemExit):
            hx711.cleanAndExit()
            reader.cleanAndExit()
        
    # Join threads to make Driver.py run till reader and hx711 complete.
    # Which should'nt be till keyboardinterrupt or system exit though :)
    reader.join()
    hx711.join()
    
if __name__ == "__main__":
    main()
