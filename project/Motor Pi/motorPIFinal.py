import urllib.parse
import requests
import http.client
import json
import time
import RPi.GPIO as GPIO






amountPerHalfTurn = 10.00  #Amount of food in grams dispensed by each half turn of the dispenser.
flowRate = 7.00 #volume of water dispensed by the pump per second ml/s


#Configuring the TB6612 motor Controller
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# set up GPIO pins ---Water Pump is Motor 1
GPIO.setup(7, GPIO.OUT) # Connected to PWMA
GPIO.setup(11, GPIO.OUT) # Connected to AIN2
GPIO.setup(12, GPIO.OUT) # Connected to AIN1
GPIO.setup(37, GPIO.OUT) # Connected to BIN1
GPIO.setup(16, GPIO.OUT) # Connected to BIN2
GPIO.setup(15, GPIO.OUT) # Connected to PWMB
GPIO.setup(13, GPIO.OUT) # Connected to STBY

#enddif Motor 1 is for Water Pump


#function that reads from the ts channel and returns a feed, including entryID
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



#Function that sends a Message to the Main Raspberry PI to Inform it that it has received the message.
def sendInfo():
    while True:
        message = "The motors have spun"
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


#Pushes instructions to the motor based on the amount of food needed to be dispensed. 
def dispenseFood(foodAmount):
    revolutions = int(foodAmount / amountPerHalfTurn)
    while(revolutions>0):
        foodMotor()
        revolutions = revolutions - 1
    sendInfo()



#Activates the Motor function for an amount of time based on the flowrate
def dispenseWater(amountWater):
    secondsPumping = amountWater/flowRate
    waterMotor(secondsPumping)
    sendInfo()
    



#Configures the GPIO pins to drive the motorA for the amount of time it takes to pump the required amount of water based on the flowrate.
def waterMotor(duration):
    GPIO.output(7, GPIO.HIGH) # Set PWMA + Set the motor speed
    GPIO.output(12, GPIO.HIGH) # Set AIN1  clockwise
    GPIO.output(11, GPIO.LOW) # Set AIN2
    GPIO.output(13, GPIO.HIGH)# Disable STBY (standby)

    # Wait while motor executes for this amount of time.
    time.sleep(duration)

    # Turn off motor
    GPIO.output(13, GPIO.LOW) # Set STBY
    GPIO.output(12, GPIO.LOW) # Set AIN1
    GPIO.output(11, GPIO.LOW) # Set AIN2
    GPIO.output(7, GPIO.LOW) # Set PWMA
    
    

#Drives motor until it rotates a half revolution, then for an instant the opposite direction to bring motor to a stop. 
def foodMotor():
    GPIO.output(16, GPIO.LOW) # Set BIN2
    GPIO.output(37, GPIO.HIGH) #Set BIN1
    GPIO.output(15, GPIO.HIGH) # Set PWMB
    # Disable STBY (standby)
    GPIO.output(13, GPIO.HIGH)
    
    time.sleep(0.46)
    
    # Reset all the GPIO pins by setting them to LOW
    
    GPIO.output(13, GPIO.LOW) # Set STBY
    GPIO.output(37, GPIO.LOW)#Set bin1
    GPIO.output(16, GPIO.LOW) # Set BIN2
    GPIO.output(15, GPIO.LOW) # Set PWMB
    
    
    
    
    
    # Motor B(coutner turn to come to a stop.
    GPIO.output(16, GPIO.HIGH) # Set BIN2
    GPIO.output(37, GPIO.LOW) #Set BIN1
    GPIO.output(15, GPIO.HIGH) # Set PWMB
    GPIO.output(13, GPIO.HIGH)#stby

   
    time.sleep(0.22)
    
    #reset
    # Reset all the GPIO pins by setting them to LOW
    GPIO.output(13, GPIO.LOW) # Set STBY
    GPIO.output(37, GPIO.LOW)#Set bin1
    GPIO.output(16, GPIO.LOW) # Set BIN2
    GPIO.output(15, GPIO.LOW) # Set PWMB
    time.sleep(2) #Wait for motor to come to a halt before continuing.




#Checks if the current command instructs passes a value that can be used to instruct the pump
def checkIfWater(field):
    
    if ((field[0] != 'None') ):
        
        amount = int(float(field[0]))
        print(amount)
        dispenseWater(amount)
    else:
        return
    
    


#Checks if the current command instructs the food pump
def checkIfFood(field):
    print
    if ((field[1]) != 'None' ):
        
        amount = int(float(field[1]))
        print(amount)
        dispenseFood(amount)
    else:
        return
    
    







currentID = readDataThingspeak()['entry_id']
#While Loop for execution
while (True):
        
        
        field = readDataThingspeak()
        
        if field['entry_id'] > (currentID): #Checks if the entryID of the feed is older than the previous one checked.
            currentID = field['entry_id']
            
            if field['field1'] == '1':  #When a message is received, intended for this PI, the code below executes.
                currentCommand = (field['field2'], field['field3']) #only relevenet command to this code is field2, field 3. THis passes a tuple to the checkIF functions
                checkIfWater(currentCommand)
                checkIfFood(currentCommand)
                
        time.sleep(1)  #TS only updates once per second so we dont need to check that often.
                
                
                
                

            
            



     
