import RPi.GPIO as GPIO
import utils.logger as logger
from config import gpio_pins_conf


SOIL_MOISTURE_PINS_LIST = [gpio_pins_conf['soil_moisture_1'],
                           gpio_pins_conf['soil_moisture_2'],
                           gpio_pins_conf['soil_moisture_3'],
                           gpio_pins_conf['soil_moisture_4']]


class SoilMoisruteSensor(object):

    def __init__(self):
        self.SENSOR_1 = SOIL_MOISTURE_PINS_LIST[0]
        self.SENSOR_2 = SOIL_MOISTURE_PINS_LIST[1]
        self.SENSOR_3 = SOIL_MOISTURE_PINS_LIST[2]
        self.SENSOR_4 = SOIL_MOISTURE_PINS_LIST[3]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SOIL_MOISTURE_PINS_LIST, GPIO.IN)


    def __do_measure(self, sensor):
        try:
            raw_value = GPIO.input(sensor)
            result = self.__recalculate(raw_value)
            logger.info('Soil moisture sensor pin: {0}. '
                        'Result: {1}'.format(sensor, result))
            return result
        except:
            logger.warning('Soil moisture sensor pin: {} FAIL')
            return -1

    def get_states(self):
        answer = dict()
        result_1 = self.__do_measure(self.SENSOR_1)
        result_2 = self.__do_measure(self.SENSOR_2)
        result_3 = self.__do_measure(self.SENSOR_3)
        result_4 = self.__do_measure(self.SENSOR_4)
        GPIO.cleanup()
        # TODO: implement as separate sensors
        answer.update({
            'status': 'success',
            'result': {
                'sensor_1': result_1,
                'sensor_2': result_2,
                'sensor_3': result_3,
                'sensor_4': result_4
            }
        })
        return answer

    def __recalculate(self, val):
        """
        DAC will be implemented here
        :param val:
        :return:
        """
        if val:
            return 0
        else:
            return 1


if __name__=='__main__':
    print SoilMoisruteSensor().get_states()
