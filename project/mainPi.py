import requests
import json
import urllib.parse
import http.client
import time


def sendMessage(
    field1=None,
    field2=None,
    field3=None,
    field4=None,
    field5=None,
    field6=None,
    field7=None,
    field8=None,
):
    key = "1EHUDJ3JAWLSDHKO"
    params = urllib.parse.urlencode(
        {
            "field1": field1,
            "field2": field2,
            "field3": field3,
            "field4": field4,
            "field5": field5,
            "field6": field6,
            "field7": field7,
            "field8": field8,
            "key": key,
        }
    )
    headers = {
        "Content-typZZe": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
    }
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        conn.close()
    except:
        print("connection failed")


def getMessage():
    url = "https://api.thingspeak.com/channels/1224435/feeds.json?api_key="
    key = "05F0ZK2NB2GHEBKO"
    header = "&results=1"

    finalURL = url + key + header

    get_data = requests.get(finalURL).json()

    channel1read = get_data["feeds"][0]

    return channel1read


def waitResponse():
    broken = 0
    while True:
        broken += 1
        if broken == 30:
            return False
        if getMessage()["entry_id"] == (currentID + 1):
            return True
        time.sleep(0.1)


currentID = getMessage()["entry_id"]

sendMessage(1, "to bailey")
if waitResponse():
    newMessage = getMessage()
    print(newMessage["field1"])
else:
    print("failed")

time.sleep(1)

sendMessage(2, "to jediael")
if waitResponse():
    newMessage = getMessage()
    print(newMessage["field1"])
else:
    print("failed")

time.sleep(1)

sendMessage(3, "to jack")
if waitResponse():
    newMessage = getMessage()
    print(newMessage["field1"])
else:
    print("failed")
