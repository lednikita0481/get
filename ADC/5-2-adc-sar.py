import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

def decimal2binary(value):
    return [int(elem) for elem in bin(value)[2:].zfill(8)]

def adc():
    value = 0
    for i in range (7, -1, -1):
        signal = decimal2binary(value + 2**i)
        GPIO.output(dac, signal)
        time.sleep(0.005)
        if GPIO.input(comp) == 1:
            value += 2**i
    return value

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 1)

try:
    while True:
        value = adc()
        number = value * (3.3 / 2**8)
        print(value, number)


finally:
    for i in dac:
        GPIO.output(i, 0)
    GPIO.cleanup()