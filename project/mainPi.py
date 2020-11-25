import requests
import urllib.parse
import http.client
import time
import sqlite3
from datetime import datetime, date

portionSize = 500
waterBowlSize = 1000
waterToFill = 0
foodToFill = 0
currentID = 0
foodStorageValue = 0
foodBowlValue = 0
waterStorageValue = 0
waterBowlValue = 0

dbconnect = sqlite3.connect("/home/pi/Documents/SYSC 3010/Labs/Project/projectdb.db")
cursor = dbconnect.cursor()


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

def checkFillFood():
    foodStorageValue = 0
    foodBowlValue = 0
    currentID = getMessage()["entry_id"]
    sendMessage(2, "to jediael 1")
    if waitResponse():
        newMessage = getMessage()
        foodBowlValue = newMessage["field2"]
        foodStorageValue = newMessage["field1"]
        print(foodStorageValue)
        print(foodBowlValue)

        foodToFill = int(portionSize) - int(foodBowlValue)
    else:
        print("failed")
        exit()

    if foodStorageValue < 1:
        print("food storage empty")
    elif foodBowlValue > 100000000:
        print("food bowl full")
    else:
        time.sleep(1)
        currentID = getMessage()["entry_id"]
        sendMessage(1, None, None, True, foodToFill)
        if waitResponse:
            print("done")
            sql = (
            "INSERT INTO tblFoodLog (amountBefore, amountFilled, time) values("
            + str(foodBowlValue)
            + ", "
            + str(foodToFill)
            + ", "
            + str(datetime.now())
            + ");"
            )
            cursor.execute(sql)
            dbconnect.commit()
            time.sleep(1)
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
        exit()

    if waterStorageValue < 1:
        print("water storage empty")
    elif waterBowlValue > 1000000000:
        print("water bowl full")
    else:
        time.sleep(1)
        currentID = getMessage()["entry_id"]
        sendMessage(1, True, waterToFill, None, None)
        if waitResponse:
            print("done")
            sql = (
            "INSERT INTO tblWaterLog (amountBefore, amountFilled, time) values("
            + str(waterBowlValue)
            + ", "
            + str(waterToFill)
            + ", "
            + str(datetime.now())
            + ");"
            )
            cursor.execute(sql)
            dbconnect.commit()
            time.sleep(1)
        else:
            print("failed")
            sql = (
            "INSERT INTO tblWaterLog (amountBefore, amountFilled, time) values("
            + str(waterBowlValue)
            + ", "
            + str(waterToFill)
            + ", "
            + str(datetime.now())
            + ");"
            )
            cursor.execute(sql)
            dbconnect.commit()
