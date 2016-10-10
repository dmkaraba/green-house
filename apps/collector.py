from handlers.sensors import DS18B20, BH1750, DHT22
from utils.mqtt_setup import GHMQTTClass


def measure_all():
    soil_temp = DS18B20().read('soil')
    air_outside_temp = DS18B20().read('air')
    luminosity = BH1750().read()
    air_inside = DHT22().read()
    return soil_temp, air_outside_temp, luminosity, air_inside


# def send_data():
#     results = measure_all()
#     msgs = [('greenhouse/soil/temperature', results[0]),
#             ('greenhouse/air/outside/temperature', results[1]),
#             ('greenhouse/luminosity', results[2]),
#             ('greenhouse/air/inside/temperature', results[3])]
#     publish(msgs)


# TODO: run in loop
# send_data()


results = measure_all()
# class MClass(GHMQTTClass):
#     def on_publish(self, mqttc, obj, mid):
#         print 'PuB'

msgs = [('greenhouse/soil/temperature', results[0]),
        ('greenhouse/air/outside/temperature', results[1]),
        ('greenhouse/luminosity', results[2]),
        ('greenhouse/air/inside/temperature', results[3])]

GHMQTTClass().pub(msgs)