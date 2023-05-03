import matplotlib.pyplot as plt
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
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)
measure = []

try:
    t_begin = time.time()
    value = adc()
    GPIO.output(troyka, 1)
    for i in range(400):
        value = adc()
        measure.append(value)
        
    GPIO.output(troyka, 0)
    for i in range(400):
        value = adc()
        measure.append(value)
 
    t_end = time.time()

    str_measure = [str(i) for i in measure]

    with open("data.txt", "w") as file:
         file.write("\n".join(str_measure))
    
    with open("settings.txt", "w") as file:
         file.write(str(1/((t_end - t_begin)/800)))

    plt.plot(measure)
    plt.show()
    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("I finished")
    print(t_end - t_begin)
    print((t_end - t_begin)/800)
