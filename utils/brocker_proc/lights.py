from handlers.controllers import Lights
from connector import GHMQTTClass
import json


class MyMQTTClass(GHMQTTClass):

    def on_message(self, mosq, obj, msg):
        # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        if msg.payload == 'on':
            Lights.set_up()
            Lights.on()
            self.publish('lights/state', json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            Lights.off()
            Lights.tear_down()
            self.publish('lights/state', json.dumps({'status': 'ok'}))
        else:
            self.publish('lights/state', json.dumps({'status': 'error'}))

    def sub(self, topic=''):
        self.on_message = self.on_message
        self.username_pw_set('bwyhxlso', 'Wna3huueUhrJ')
        self.connect("m21.cloudmqtt.com", 10990, 60)
        self.subscribe(topic, 0)
        self.loop_forever()
          # rc = 0
          # while rc == 0:
          #     rc = self.loop()
          # return rc

MyMQTTClass().sub('lights/')