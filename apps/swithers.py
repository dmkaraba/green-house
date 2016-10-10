from handlers.controllers import Lights, Fan, Pump, Servo
from utils.mqtt_setup import GHMQTTClass


class MyMQTTClass(GHMQTTClass):

    def on_lights_on(self, mosq, obj, msg):
        Lights.set_up()
        Lights.on()

    def on_lights_off(self, mosq, obj, msg):
        Lights.off()
        Lights.tear_down()

    def on_message(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def sub(self):
        self.message_callback_add("lights/on", self.on_lights_on)
        self.message_callback_add("lights/off", self.on_lights_off)
        self.on_message=self.on_message
        self.username_pw_set('bwyhxlso', 'Wna3huueUhrJ')
        self.connect("m21.cloudmqtt.com", 10990, 60)
        self.subscribe("lights/#", 0)
        self.loop_forever()
        # rc = 0
        # while rc == 0:
        #     rc = self.loop()
        # return rc

MyMQTTClass().sub()
