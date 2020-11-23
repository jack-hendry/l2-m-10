import requests
import urllib.parse
import http.client
import time
import sqlite3
from datetime import datetime, date

portionSize = 500
fullWaterWeight = 1000
waterToFill = 0
foodToFill = 0
currentID = 0

""" dbconnect = sqlite3.connect("/home/pi/Documents/SYSC 3010/Labs/Project/projectdb.db")
cursor = dbconnect.cursor() """


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


def test():
    currentID = getMessage()["entry_id"]
    sendMessage(3, "to jack 1")
    if waitResponse():
        newMessage = getMessage()

        waterBowlValue = newMessage["field2"]
        waterStorageValue = newMessage["field1"]

        print("water storage value:" + str(waterStorageValue))
        print("water bowl value:" + str(waterBowlValue))

        waterToFill = int(fullWaterWeight) - int(waterBowlValue)

        """ sql = (
            "INSERT INTO tblWaterLog (amountBefore, amountFilled, time) values("
            + str(waterBowlValue)
            + ", "
            + str(waterToFill)
            + ", "
            + str("today")
            + ");"
        )
        cursor.execute(sql)
        dbconnect.commit() """

    else:
        print("failed")

    time.sleep(2)

    # storage field 1
    # weight field 2
    currentID = getMessage()["entry_id"]
    sendMessage(2, "to jediael 1")
    if waitResponse():
        newMessage = getMessage()

        foodBowlValue = newMessage["field2"]
        foodStorageValue = newMessage["field1"]

        print("food storage value:" + str(foodStorageValue))
        print("food bowl value:" + str(foodBowlValue))

        foodToFill = int(portionSize) - int(foodBowlValue)

        """ sql = (
            "INSERT INTO tblFoodLog (amountBefore, amountFilled, time) values("
            + str(foodBowlValue)
            + ", "
            + str(foodToFill)
            + ", "
            + str(datetime.now())
            + ");"
        )
        cursor.execute(sql)
        dbconnect.commit() """
    else:
        print("failed")

    time.sleep(2)

    currentID = getMessage()["entry_id"]
    sendMessage(1, waterToFill, foodToFill, "to bailey")
    if waitResponse():
        newMessage = getMessage()
        print(newMessage["field1"])
    else:
        print("failed")


def checkFillFood():
    currentID = getMessage()["entry_id"]
    sendMessage(2, "to jediael 1")
    if waitResponse():
        newMessage = getMessage()

        foodBowlValue = newMessage["field2"]
        foodStorageValue = newMessage["field1"]

        foodToFill = int(portionSize) - int(foodBowlValue)
    else:
        print("failed")

    if foodStorageValue < 100:
        print("food storage empty")
    elif foodBowlValue > 101:
        print("food bowl full")
    else:
        currentID = getMessage()["entry_id"]
        sendMessage(1, None, None, True, foodToFill)
        if waitResponse:
            print("done")
        else:
            print("failed")


def checkFillWater():
    currentID = getMessage()["entry_id"]
    sendMessage(3)
    if waitResponse():
        newMessage = getMessage()

        waterBowlValue = newMessage["field2"]
        waterStorageValue = newMessage["field1"]

        waterToFill = int(waterBowlSize) - int(waterBowlValue)
    else:
        print("failed")

    if waterStorageValue < 100:
        print("water storage empty")
    elif waterBowlValue > 400:
        print("water bowl full")
    else:
        currentID = getMessage()["entry_id"]
        sendMessage(1, True, waterToFill, None, None)
        if waitResponse:
            print("done")
        else:
            print("failed")
