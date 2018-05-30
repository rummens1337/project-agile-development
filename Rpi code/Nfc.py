#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import threading
import time
import requests

class Read(threading.Thread):
    GPIO.setwarnings(False)
    
    def run(self):
        print ("Nfc.py = Enabled")
        continue_reading = True
        MIFAREReader = MFRC522.MFRC522()
        
        def cleanAndExit(self):
            global continue_reading
            print ("Ctrl+C captured, ending read.")
            continue_reading = False
            GPIO.cleanup()
            sys.exit()
        
        def arrayToString(self,array):
            return ''.join(str(e) for e in array)
        
        def checkCard(card):
            if (card == "12312436217250"):
                print("Sending NFC data to mendix.. Data = Enable login for user Rummens#5123")
                
##                    headers = {'Content-Type': 'application/json'}
##                    URL = 'https://2018et08publisheds.mxapps.io/rest/Published_REST_service/Beer'
##                    payload = "{\n\t\"Beer\": " + str(gram) + "}"
##                    
##                    response = requests.request("PUT", URL, data=payload, headers=headers)
##                    print(response)
                
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while continue_reading:
            #keeps cpu usage low
            time.sleep(0.5)
            
            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == MIFAREReader.MI_OK:
                print ("Card detected")
    
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:
                card = arrayToString(self,uid)
                checkCard(card)
                
                