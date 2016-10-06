import Adafruit_DHT as dht
import utils.logger as logger
from config import gpio_pins_conf
from measurements import BaseSensor


class DHT22(BaseSensor):

    DHT22_PIN = gpio_pins_conf['DHT22']

    @classmethod
    def do_measure(cls):
        answer = dict()
        try:
            h, t = dht.read_retry(dht.DHT22, cls.DHT22_PIN, delay_seconds=3)
            h, t = float("%.1f" % h), float("%.1f" % t)
            logger.info('DHT22 asked. T: {}, H: {}'.format(t, h))
            answer.update({'status': 'success',
                           'result': {'temperature': t, 'humidity': h}})
        except:
            answer.update({'status': 'fail'})
            logger.warning('DHT22 fail')
        return answer

