import urllib.parse
import requests
import http.client
import json
import time
import RPi.GPIO as GPIO
import threading
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
    wt = max(0, int(hx.get_weight(5)))
    return wt

def getDistance():
    ht = hc.distance()
    return ht

currentID = readData()['entry_id']
while True:
    field = readData()
    if field['entry_id'] == (currentID+1):
        currentID += 1
        if field['field1'] == '3':
            grams = getWeight()
            time.sleep(0.1)
            distance = getDistance()
            sendData(distance, grams)
            time.sleep(1)
            print("Distance and Weight sent")
            print(field['field2'])
            continue
