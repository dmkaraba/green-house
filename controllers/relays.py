from time import sleep
import RPi.GPIO as GPIO
from config import gpio_pins_conf
import utils.logger as logger


RELAY_PIN_1 = gpio_pins_conf['relay_1']
RELAY_PIN_2 = gpio_pins_conf['relay_2']
RELAY_PIN_3 = gpio_pins_conf['relay_3']
RELAY_PIN_4 = gpio_pins_conf['relay_4']

channels = [RELAY_PIN_1, RELAY_PIN_2, RELAY_PIN_3, RELAY_PIN_4]

GPIO.setmode(GPIO.BCM)
GPIO.setup(channels, GPIO.OUT, initial=GPIO.HIGH)

for i in range(5):
    sleep(0.1)
    GPIO.output(RELAY_PIN_1, GPIO.LOW)
    sleep(0.1)
    GPIO.output(RELAY_PIN_2, GPIO.LOW)
    sleep(0.1)
    GPIO.output(RELAY_PIN_3, GPIO.LOW)
    sleep(0.1)
    GPIO.output(RELAY_PIN_4, GPIO.LOW)
    sleep(0.1)
    GPIO.output(RELAY_PIN_1, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(RELAY_PIN_2, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(RELAY_PIN_3, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(RELAY_PIN_4, GPIO.HIGH)

GPIO.cleanup()

# TODO: write a swich, on, off methods