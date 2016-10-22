#!/usr/bin/python
# GPIO.BCM mode

gpio_pins_conf={
    'DHT22': 18,
    'servo': 17,
    'soil_moisture_1': 5,
    'soil_moisture_2': 6,
    'soil_moisture_3': 13,
    'soil_moisture_4': 16,
    'relay_lights': 19,
    'relay_fans': 26,
    'relay_pump_1': 20,
    'relay_pump_2': 21,
}

sensor_ids={
    'ds18b20_a': '28-0000076aa408',
    'ds18b20_b': '28-0000076bb328'
}

mqtt_topics_sub={
    'lights': 'lights/',
    'fans': 'fans/',
    'pumps': 'pumps/',
    'servo': 'window/'
}

mqtt_topics_pub={
    'lights': 'lights/status',
    'fans': 'fans/status',
    'pumps': 'pumps/status',
    'servo': 'window/status',
}
cloud_mqtt_cred={
    'user': 'bwyhxlso',
    'pass': 'Wna3huueUhrJ',
    'server': 'm21.cloudmqtt.com'
}

mongodb_conf={
    'host': 0,
    'port': 0,
    'db_name': 'greenhouse',
    'conditions_coll': 'conditions',
    'plants_coll': 'plants'
}
