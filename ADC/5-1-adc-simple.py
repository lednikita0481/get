import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

def decimal2binary(value):
    return [int(elem) for elem in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.005)
        number = value * (3.3 / 2**8)
        if GPIO.input(comp) == 0:
            break
    GPIO.output(dac, signal)
    return value

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

try:
    while True:
        value = adc()
        number = value * (3.3 / 2**8)
        print(value, number)


finally:
    for i in dac:
        GPIO.output(i, 0)
    GPIO.cleanup()

