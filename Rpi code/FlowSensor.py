import serial
import time
import threading
import requests


class Measure(threading.Thread):
 
     # Called when Driver.py aborts.
    def cleanAndExit(self):
        global ser
        print("Cleaning...")
        ser.close()
        print("Bye!")
        sys.exit()
        
    def run(self):
        print("FlowSensor.py = Enabled")
        # Initializes serial port connection via USB 0 with a boundrate of 9600.
        ser = serial.Serial('/dev/ttyACM0', 9600)
        # Makes sure only 1 keg of beer is removed from stock.
        switch = 0
        oldIntMessage = 0
        
        while(True):
            
            try:
            
                time.sleep(3)
                message = ser.readline()
                decodedMessage = (message.decode('utf-8'))
                intMessage = int(message)
                # Flushes Arduino's serial buffer, so only 'last' data is read.
                ser.flushInput()
                # Prevents from reading an empty buffer.
                time.sleep(1.5)
                
                if(intMessage != oldIntMessage):
                    print("Sending flowdata to mendix.. Data = ", intMessage)
                    
                    headers = {'Content-Type': 'application/json'}
                    URL = 'https://2018et08publisheds.mxapps.io/rest/Published_REST_service/Beer'
                    payload = "{\n\t\"Beer\": " + str(intMessage) + "}"
                    
                    response = requests.request("PUT", URL, data=payload, headers=headers)
                    print(response)
                
                # Sets oldIntMessage = intMessage, so above IF statement is only executed once per change.
                oldIntMessage = intMessage
                
                # If Arduino is reset, turns switch back to 0.
                if(intMessage == 100000):
                    switch = 0
                
                if(intMessage < 99600 and switch == 0):
                    print("Removing 1 keg beer from stock...")
                    switch = 1 # Makes sure this function is only called once per keg.
                
            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()                