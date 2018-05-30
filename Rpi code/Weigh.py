import RPi.GPIO as GPIO
import time
import sys
from HX711 import HX711
import threading
import requests


class Scale(threading.Thread):
    
    # Called when Driver.py aborts.
    def cleanAndExit(self):
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
        sys.exit()
    
    def run(self):
        print("Weigh.py = Enabled")
        # Set datapins to 16 & 18.
        hx = HX711(16, 18)
        hx.set_reading_format("LSB", "MSB")
        
        # With a reference_unit of 420, returns value in Grams.
        hx.set_reference_unit(420)
        hx.reset()
        hx.tare()
        
        val = 0
        oldgram = 0
        
        while True:
            
            try:
                
                # Calculates average of 30 weighs.
                val = hx.get_weight(30)
                gram = (round(-val))
                
                if((gram < (oldgram -10)) or (gram > (oldgram +10))):
                    print("Sending Weighdata to mendix.. Data = ", gram)

##                    headers = {'Content-Type': 'application/json'}
##                    URL = 'https://2018et08publisheds.mxapps.io/rest/Published_REST_service/Beer'
##                    payload = "{\n\t\"Beer\": " + str(gram) + "}"
##                    
##                    response = requests.request("PUT", URL, data=payload, headers=headers)
##                    print(response)
                
                # Sets oldgram = gram, so above IF statement is only executed once per change.
                oldgram = gram
                
                hx.power_down()
                hx.power_up()
                
            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()