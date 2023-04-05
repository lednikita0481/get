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

def leds_output(voltage):
    max_voltage = 0.82
    out = [0]*8
    for i in range(1, 9):
        if voltage > max_voltage * i/8:
            out[i-1] = 1
    out = list(reversed(out))
    GPIO.output(leds, out)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 1)

try:
    while True:
        value = adc()
        number = value * (3.3 / 2**8)
        print(value, number)
        leds_output(number)


finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()