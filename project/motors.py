import urllib.parse
import requests
import http.client
import json
import time


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


#Creates a PWM signal using the data from the pumpWater() or dispenseFood() function
def pwmSignal(value):
    print('1')





#Checks if the current command instructs water pump
def checkIfWater():
    if ((currentCommand['field2'] != None) and (currentCommand['field3'] != None)):
        print('1')






#Checks if the current command instructs the food pump
def checkIfFood():
    if ((currentCommand['field3'] !=0) and (currentCommand['field4'] != 0)):
        #dispenseFood()
        print('1')


    
    





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
            time.sleep(3)

            
            



     
