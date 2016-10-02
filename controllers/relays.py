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
    RELAY = gpio_pins_conf['relay_1']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY, GPIO.OUT, initial=GPIO.HIGH)


class Pump(RelayBase):
    pass


class Fan(RelayBase):
    pass
