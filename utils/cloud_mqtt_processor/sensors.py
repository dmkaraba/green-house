from handlers.sensors import DS18B20, BH1750, DHT22
from connector import GHMQTTClass


def pub_all():

    def measure_all():
        soil_temp = DS18B20('soil').read()
        air_outside_temp = DS18B20('air').read()
        luminosity = BH1750().read()
        air_inside = DHT22().read()
        return soil_temp, air_outside_temp, luminosity, air_inside

    results = measure_all()

    msgs = [('greenhouse/soil/temperature', results[0]),
            ('greenhouse/air/outside/temperature', results[1]),
            ('greenhouse/luminosity', results[2]),
            ('greenhouse/air/inside/temperature', results[3])]

    GHMQTTClass().pub(msgs)


if __name__=='__main__':
    pub_all()
