#!/usr/bin/python

from handlers.sensors import DS18B20, BH1750, DHT22


def pull_data():
    attempts = 3
    while attempts:
        try:
            DS18B20_soil_result = DS18B20('soil').read()
            DS18B20_air_result = DS18B20('air').read()
            BH1750_result = BH1750().read()
            DHT22_result = DHT22().read()
            return (DS18B20_soil_result,
                    DS18B20_air_result,
                    BH1750_result,
                    DHT22_result)
        except:
            attempts = attempts - 1
    return None


def read_all():
    raw_data = pull_data()
    if raw_data:
        soil_temperature = raw_data[0].get('result', None)
        air_out_temperature = raw_data[1].get('result', None)
        luminosity = raw_data[2].get('result', None)
        air_temperature_inside = raw_data[3].get('result', dict()).get('temperature', None)
        air_humudity_inside = raw_data[3].get('result', dict()).get('humidity', None)
        data = {
            'soil_temperature': soil_temperature,
            'air_out_temperature': air_out_temperature,
            'luminosity': luminosity,
            'air_inside': {'temperature': air_temperature_inside,
                           'humidity': air_humudity_inside}
        }
        result = {'status': 'success', 'result': data}
        return result
    else:
        return None


if __name__=='__main__':
    print read_all()
