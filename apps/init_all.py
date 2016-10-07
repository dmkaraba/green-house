from handlers.sensors import DS18B20, BH1750, DHT22
from handlers.controllers import Lights, Fan, Servo
import time

print DS18B20('air').do_measure()
print DS18B20('soil').do_measure()
print BH1750().do_measure()
print DHT22.do_measure()

# print Fan.on()
# print Lights.on()
# time.sleep(1)
#
# print Fan.off()
# print Lights.off()
# time.sleep(1)
#
# print Fan.switch()
# print Lights.switch()
# time.sleep(1)
#
# Fan.tear_down()
#
#
# print Servo.set_state(0)
# time.sleep(1)
# print Servo.set_state(5)
# time.sleep(1)
# print Servo.set_state(10)
# time.sleep(1)
# print Servo.set_state(5)
# time.sleep(1)
# print Servo.set_state(20)
