#!/usr/bin/python
from utils.sensors.reader import read_all
from utils.cloud_mqtt_processor import GHMQTTClass
# TODO: delete this file

def pub_all():

    results = read_all()
    data = results['result']

    msgs = [
            ('conditions/luminosity', data['luminosity']),
            ('conditions/soil/temperature', data['soil_temperature']),
            ('conditions/air/outside/temperature', data['air_out_temperature']),
            ('conditions/air/inside/temperature', data['air_inside']['temperature']),
            ('conditions/air/inside/humidity', data['air_inside']['humidity'])
    ]

    GHMQTTClass().pub(msgs)


if __name__=='__main__':
    pub_all()
