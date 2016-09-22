import Adafruit_DHT as dht
from config import gpio_pins_conf
import utils.logger as logger


DHT22_PIN = gpio_pins_conf['DHT22']

class DHT22_sensor(object):

    @classmethod
    def get_state(self):
        answer = dict()
        try:
            h, t = dht.read_retry(dht.DHT22, DHT22_PIN, delay_seconds=3)
            h = float("%.1f" % h)
            t = float("%.1f" % t)
            logger.info('DHT22 asked. T: {}, H: {}'.format(t, h))
            answer.update({'status': 'success',
                           'result': {'temperature': t, 'humidity': h}})
        except:
            answer.update({'status': 'fail'})
            logger.warning('DHT22 fail')
        return answer


if __name__=='__main__':
    print DHT22_sensor.get_state()