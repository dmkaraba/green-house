#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from config import gpio_pins_conf
import utils.logger as logger


class RelayBase(object):

    RELAY = None

    @classmethod
    def on(cls):
        GPIO.output(cls.RELAY, GPIO.LOW)
        return {'status': 'success', 'result': True}

    @classmethod
    def off(cls):
        GPIO.output(cls.RELAY, GPIO.HIGH)
        return {'status': 'success', 'result': False}

    @classmethod
    def switch(cls):
        switched_state = not GPIO.input(cls.RELAY)
        GPIO.output(cls.RELAY, switched_state)
        return {'status': 'success', 'result': switched_state}

    @classmethod
    def get_state(cls):
        state = not GPIO.input(cls.RELAY)
        return {'status': 'success', 'result': state}

    @classmethod
    def tear_down(cls):
        GPIO.cleanup()
        return {'status': 'success', 'result': {}}


class Lights(RelayBase):
    RELAY = gpio_pins_conf['relay_lights']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY, GPIO.OUT, initial=GPIO.HIGH)


class Fan(RelayBase):
    RELAY = gpio_pins_conf['relay_fans']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY, GPIO.OUT, initial=GPIO.HIGH)


class Pump(RelayBase):
    pass


if __name__=='__main__':
    Fan.on()
    Lights.on()
    time.sleep(2)

    Fan.off()
    Lights.off()
    time.sleep(2)

    Fan.on()
    Lights.on()
    time.sleep(2)

    Fan.tear_down()
    Lights.tear_down()