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


def measure_dist():
    d = hc.distance()
    return d


def measure_wt():
    val = max(0, int(hx.get_weight(5)))
    return val


while True:
    time.sleep(0.1)
    x = measure_dist()
    time.sleep(0.1)
    y = measure_wt()
    print("Distance: %.2f cm" % x + " and Weight: %.2f" % y)
