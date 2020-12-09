import urllib.parse
import requests
import http.client
import json
import time
import RPi.GPIO as GPIO
from hx711 import HX711
from hcsr04 import HCSR04

GPIO.setwarnings(False)
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(95.20)
hx.reset()
hx.tare()

hc = HCSR04(18, 24)


def readData():
    
    """
    Get messages from ThingSpeak channel
    Returns:
        (list)field1: messages from field 1 of ThingSpeak
    """
    
    URl='https://api.thingspeak.com/channels/1173908/feeds.json?api_key=6G647UFZ4V0F7XL2&results=2'
    KEY='6G647UFZ4V0F7XL2'
    HEADER='&results=1'
    NEW_URL = URl+KEY+HEADER
    #print(NEW_URL)
    
    get_data=requests.get(NEW_URL).json()
    #print(get_data)
    
    channel_id=get_data['channel']['id']
    
    field1 = get_data['feeds'][0]
    #print(field1)
    
    return (field1)     

    
    
keySend = "AB2DLL1XSNYHIU2O"
def sendData(dist,wt):
    """
    Send messages to ThingSpeak channel

    Parameters:
        (float) dist: distance from ultrasonic sensor
        (float) wt: weight from weight sensor
    """
    while True:
        params = urllib.parse.urlencode({'field1': dist, 'field2': wt, 'key': keySend })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(response.status, response.reason)
            data = response.read()
            conn.close()
            break
        except:
            print ("connection failed")
            break

def getWeight():
    """
    Gets weight from weight sensor in real-time
    :return:
        (float) wt: weight from sensor
    """
    wt = max(0.00, float(hx.get_weight(5)))
    return wt

def getDistance():
    """
    Gets distance from ultrasonic sensor in real-time
    :return:
        (float) ht: distance measured by ultrasonic sensor
    """
    ht = hc.distance()
    return ht

def checkHardware():
    """
    Checks if sensors are connected and ready to use
    :return:
        (float) ht: distance measured by ultrasonic sensor
        (float) wt: weight from sensor
    """
    checkwt = getWeight()
    checkht = getDistance()
    if(isinstance(checkwt,float) == False):
        print("Weight sensor is disconnected")
        return False
    elif(isinstance(checkht,float)== False):
        print("Ultrasonic sensor is disconnected")
        return False
    else:
        print("System is ready")
        return True


currentID = readData()['entry_id']
if __name__ == "__main__":
    if(checkHardware() == True):
        while True:
            field = readData()
            if field['entry_id'] == (currentID+1):
                currentID += 1
                if field['field1'] == '2':
                    grams = round(getWeight(),2)
                    time.sleep(0.5)
                    distance = round(getDistance(),2)
                    sendData(distance, grams)
                    time.sleep(1)
                    print("Distance: %.2f and "%distance + "Weight: %.2f sent"%grams)
                    print(field['field2'])
                    continue
