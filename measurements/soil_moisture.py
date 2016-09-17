import RPIO
import time


RPIO.setmode(RPIO.BOARD)
RPIO.setup(11, RPIO.IN)
for i in range(10):
    print RPIO.input(11)
    time.sleep(1)
RPIO.cleanup()
