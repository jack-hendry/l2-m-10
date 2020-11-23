import urllib.parse
import requests
import http.client
import json
import time
import RPi.GPIO as GPIO

amountPerHalfTurn = 10.00  #Amount of food in grams dispensed by each half turn of the dispenser.
flowRate = 10.00 #volume of water dispensed by the pump per second
timeForHalfTurn = 10.00 #amount of time it takes to turn the motor a half revolution.

#Configuring the TB6612 motor Controller
GPIO.setmode(GPIO.BOARD)

# set up GPIO pins ---Water Pump is Motor 1
GPIO.setup(7, GPIO.OUT) # Connected to PWMA
GPIO.setup(11, GPIO.OUT) # Connected to AIN2
GPIO.setup(12, GPIO.OUT) # Connected to AIN1
GPIO.setup(37, GPIO.OUT) # Connected to BIN1
GPIO.setup(16, GPIO.OUT) # Connected to BIN2
GPIO.setup(15, GPIO.OUT) # Connected to PWMB
GPIO.setup(13, GPIO.OUT) # Connected to STBY


#enddif Motor 1 is for Water Pump



key = "AB2DLL1XSNYHIU2O"
def readDataThingspeak():
    URl='https://api.thingspeak.com/channels/1173908/feeds.json?api_key=6G647UFZ4V0F7XL2&results=2'
    KEY='6G647UFZ4V0F7XL2'
    HEADER='&results=1'
    NEW_URL = URl+KEY+HEADER
    get_data = requests.get(NEW_URL).json()
    channel_id=get_data['channel']['id']
    field1 = get_data['feeds'][0]
    return (field1)


def sendInfo():
    while True:
        message = "The messaged was received by Pi-Motor and the Motors are executing their sequence"
        params = urllib.parse.urlencode({'field1': message,'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            
            print (response.status, response.reason)
            data = response.read()
            conn.close()
            break
        except:
            #print ("connection failed")
            break




def dispenseFood(foodAmount):
    revolutions = int(foodAmount / amountPerHalfTurn)
    while(revolutions>0):
        foodMotor()
        revolutions = revolutions - 1




def dispenseWater(amountWater):
    secondsPumping = amountWater/flowRate
    waterMotor(secondsPumping)



#Configures the GPIO pins to drive the motorA for the amount of time it takes to pump the required amount of water based on the flowrate.
def waterMotor(duration):
    GPIO.output(7, GPIO.HIGH) # Set PWMA + Set the motor speed
    GPIO.output(12, GPIO.HIGH) # Set AIN1  clockwise
    GPIO.output(11, GPIO.LOW) # Set AIN2
    GPIO.output(13, GPIO.HIGH)# Disable STBY (standby)

    # Wait while motor executes Motor executes for this amount of time.
    time.sleep(duration)

    # Turn off motor
    GPIO.output(13, GPIO.LOW) # Set STBY
    GPIO.output(12, GPIO.LOW) # Set AIN1
    GPIO.output(11, GPIO.LOW) # Set AIN2
    GPIO.output(7, GPIO.LOW) # Set PWMA
    
    

#Configures the GPIO pins to drive the motorB for the amount of time it takes to complete half of a revolution   
def foodMotor():
    GPIO.output(37, GPIO.HIGH) # Set BIN1
    GPIO.output(16, GPIO.LOW) # Set BIN2

    GPIO.output(15, GPIO.HIGH) # Set PWMB
    GPIO.output(13, GPIO.HIGH) #Disable STBY

    #Spin the motors for the Amount of time it takes to spin a half revolution.
    time.sleep(timeForHalfTurn)


    #Turn off Motor.    
    GPIO.output(37, GPIO.LOW) # Set BIN1
    GPIO.output(16, GPIO.LOW) # Set BIN2
    GPIO.output(15, GPIO.LOW) # Set PWMB
    GPIO.output(13, GPIO.LOW) # Set STBY
    time.sleep(0.25)










#Checks if the current command instructs water pump
def checkIfWater():
    if ((currentCommand['field2'] != None) and (currentCommand['field3'] != None)):
        dispenseWater(currentCommand['field3'])


#Checks if the current command instructs the food pump
def checkIfFood():
    if ((currentCommand['field4'] !=None) and (currentCommand['field5'] != None)):
        dispenseFood(currentCommand['field5'])





#While Loop for execution
while True: 
    currentID = readDataThingspeak()['entry_id']
    field = readDataThingspeak()
    
    if field['entry_id'] >= (currentID): 
        currentID = field['entry_id'] 
        if field['field1'] == '1':  #When a message is received, intended for this PI, the code below executes.
            
            currentCommand = field
            sendInfo()
            print(field['field2'])
            print(field['field3'])
            time.sleep(3)

            
            



     