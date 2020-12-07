import requests
import urllib.parse
import http.client
import time
import sqlite3
from datetime import datetime, date
import smtplib
from tkinter import *
from tkinter.ttk import Combobox

portionSize = 500
waterBowlSize = 1000
waterToFill = 0
foodToFill = 0
currentID = 0
foodStorageValue = 0
foodBowlValue = 0
waterStorageValue = 0
waterBowlValue = 0
email = ""

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
        if broken == 60:
            return False
        if getMessage()["entry_id"] == (currentID + 1):
            return True
        time.sleep(0.1)


def sendMail(subject, body, email):
    GMAIL_USERNAME = "FitPet3010@gmail.com"  # change this to match your gmail account
    GMAIL_PASSWORD = "fitpet2020!!"
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        msg = f"Subject: {subject}\n\n{body}"
        smtp.sendmail(GMAIL_USERNAME, email, msg)


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

    if foodStorageValue > 16:
        sendMail(
            "FitPet Notice", "The food storage is empty in your FitPet system.", email
        )
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
        sendMail(
            "FitPet Notice", "The water storage is empty in your FitPet system.", email
        )
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

class MyWindow:
    def __init__(self, win):
        self.lbl5 = Label(win, text = "Type of pet:")
        self.lbl5.place(x=0, y=0)
        self.v1= StringVar()
        self.v1.set(1)
        self.catRB = Radiobutton(win, text="Cat", variable=self.v1,value="Cat")
        self.dogRB = Radiobutton(win, text="Dog", variable=self.v1,value= "Dog")
        self.catRB.place(x=150, y=0)
        self.dogRB.place(x=200, y=0)
        self.lbl6 = Label(win, text = "Sex of pet: ")
        self.lbl6.place(x=0, y=50)
        self.v4 = StringVar() 
        self.v4.set(1)
        self.maleRB = Radiobutton(win, text="Male ", variable=self.v1,value="Male")
        self.femaleRB = Radiobutton(win, text="Female ", variable=self.v1,value="Female")
        self.maleRB.place(x=150, y=50)
        self.femaleRB.place(x=200, y=50)
        self.lbl4 = Label(win, text = "Size of Breed:")
        self.lbl4.place(x=0, y=100)
        self.v2= StringVar()
        self.v2.set(1)
        self.smallBreedRB = Radiobutton(win, text="Small", variable=self.v2,value="Small")
        self.mediumBreedRB = Radiobutton(win, text="Medium", variable=self.v2,value= "Medium")
        self.largeBreedRB = Radiobutton(win, text="Large", variable=self.v2,value= "Medium")
        self.smallBreedRB.place(x=150, y=100)
        self.mediumBreedRB.place(x=210, y=100)
        self.largeBreedRB.place(x= 285, y=100)
        self.lbl1=Label(win, text='Pets Name: ')
        self.lbl1.place(x=0, y=150)
        self.t1=Entry(bd=3)
        self.t1.place(x=150, y=150)
        self.lbl2=Label(win, text='Pet Owners Email address:')
        self.lbl2.place(x=0, y=200)
        self.t2=Entry()
        self.t2.place(x=150, y=200)
        self.foodAmount =Label(win, text='Daily Amount of Food:')
        self.foodAmount.place(x=0, y=250)
        self.t4=Entry()
        self.t4.place(x=150, y=250)
        self.lbl3=Label(win, text='Number of meals/day: ')
        self.lbl3.place(x=0, y=300)
        self.v0=IntVar()
        self.v0.set(1)
        self.r1 = Radiobutton(win, text="2", variable=self.v0,value=2)
        self.r2 = Radiobutton(win, text="3", variable=self.v0,value=3)
        self.r3 = Radiobutton(win, text="4", variable=self.v0,value=4)
        self.r4 = Radiobutton(win, text="5", variable=self.v0,value=5)
        self.r1.place(x=150, y=300)
        self.r2.place(x=200,y=300)
        self.r3.place(x=250,y=300)
        self.r4.place(x=300,y=300)
        self.b1=Button(win, text='Submit', command = self.submit)
        self.b1.place(x=150, y=350)

    def submit(self): # input 2 variables 
        typePet = self.v1.get()
        breedSize = self.v2.get()
        petName = self.t1.get()
        ownerEmail = self.t2.get()
        setNumberMeals =int( self.v0.get() )
        sexOfPet = self.v4.get()
        dailyFood = int(self.t4.get()) 
        #testing purposes 
        print( typePet + " " + sexOfPet +"  " + breedSize + " " + petName +"  " + ownerEmail + " "
        + str(dailyFood) + " " + str(setNumberMeals)  )


def baileyTest():
    currentID = getMessage()["entry_id"]
    sendMessage(1, None, 50)
    print(waitResponse())

    currentID = getMessage()["entry_id"]
    sendMessage(1, 35, None)
    print(waitResponse())

window=Tk()
mywin=MyWindow(window)
window.title('Hello Python')
window.geometry("500x400+10+10")
window.mainloop()

baileyTest()

while True:
    exit()
