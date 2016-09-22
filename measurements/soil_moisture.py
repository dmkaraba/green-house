import RPi.GPIO as GPIO
from config import gpio_pins_conf
import time


SOIL_MOISTURE_PINS_LIST = [gpio_pins_conf['soil_moisture_a'],]


class SoilMoisruteSensor(object):

    @staticmethod
    def get_state():
        answer = dict()
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(SOIL_MOISTURE_PINS_LIST, GPIO.IN)
            raw_value_a = GPIO.input(SOIL_MOISTURE_PINS_LIST[0])
            result_a = SoilMoisruteSensor.recalculate(raw_value_a)
            GPIO.cleanup()
            answer.update({
                            'status': 'success',
                            'result': {
                                        'sensor_a': result_a,
                                        'sensor_b': result_a,
                                        'sensor_c': result_a,
                                        'sensor_d': result_a
                                        }
            })
        except:
            answer.update({'status': 'fail'})
        return answer

    @staticmethod
    def recalculate(val):
        if val:
            return 0
        else:
            return 1


if __name__=='__main__':
    print SoilMoisruteSensor.get_state()