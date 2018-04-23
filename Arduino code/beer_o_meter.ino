#include <SevSeg.h>
/**
 * Declaration of display
 */
SevSeg sevseg; //Initiate a seven segment controller object

/**
 * Declaration of flowsensor
 */
byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin       = 2;
byte inputPin        = 1;

// The hall-effect flow sensor outputs approximately 4.5 pulses per second per Litre/Minute of flow.
// **Michel** The waterflow sensor has different pulseCounts at different waterflow speeds, therefore making it inaccurate. 
// However, i find a calibrationFactor of 5.5 to be fairly accurate.

// An option (to fix this somewhat) would be to count average of waterflow / minute 
// opposed to actual waterflow / minute, and create a better factor. But that is quite out of the scope of this project.
float calibrationFactor = 5.5;

volatile byte pulseCount;  
float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;
unsigned long oldTime;

void setup()
{
  /**
   * Setup of flowsensor
   */
  
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;

  // The Hall-effect sensor is connected to pin 2 which uses interrupt 0.
  // Configured to trigger on a FALLING state change (transition from HIGH
  // state to LOW state)
  attachInterrupt(sensorInterrupt, pulseCounter_ISR, FALLING);

  /**
   * Setup of display
   */
  byte numDigits = 4;
  byte digitPins[] = {13, 3, 4, 5};
  byte segmentPins[] = {6, 7, 8, 9, 10, 11, 12,14};
  sevseg.begin(COMMON_ANODE, numDigits, digitPins, segmentPins);
  sevseg.setBrightness(90);
}

/**
 * Main program loop
 */
void loop()
{
   
   if((millis() - oldTime) > 1000)    // Only process counters once per second
  { 
    // Disable the interrupt while calculating flow rate and sending the value to
    // the host
    detachInterrupt(sensorInterrupt);
        
    // Because this loop may not complete in exactly 1 second intervals we calculate
    // the number of milliseconds that have passed since the last execution and use
    // that to scale the output. We also apply the calibrationFactor to scale the output
    // based on the number of pulses per second per units of measure (litres/minute in
    // this case) coming from the sensor.
    flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
    
    // Note the time this processing pass was executed. Note that because we've
    // disabled interrupts the millis() function won't actually be incrementing right
    // at this point, but it will still return the value it was set to just before
    // interrupts went away.
    oldTime = millis();
    
    // Divide the flow rate in litres/minute by 60 to determine how many litres have
    // passed through the sensor in this 1 second interval, then multiply by 1000 to
    // convert to millilitres.
    flowMilliLitres = (flowRate / 60 * 1000);
    
    // Add the millilitres passed in this second to the cumulative total
    totalMilliLitres += flowMilliLitres;
      
    unsigned int frac;

    unsigned long vatBier = 100000;
    unsigned long printML = ((vatBier - totalMilliLitres)/100);
    sevseg.setNumber(printML,1);

    // Reset the pulse counter so we can start incrementing again
    pulseCount = 0;
    
    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(sensorInterrupt, pulseCounter_ISR, FALLING);
  }
  sevseg.refreshDisplay(); // Must run repeatedly
}

/*
Interrupt Service Routine
 */
void pulseCounter_ISR()
{
  // Increment the pulse counter
  pulseCount++;
}
