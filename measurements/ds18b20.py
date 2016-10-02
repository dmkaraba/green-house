import time
from config import sensor_ids
import utils.logger as logger


SENSOR_A = sensor_ids['ds18b20_a']
SENSOR_B = sensor_ids['ds18b20_b']


# def gettemp(id):
# 	try:
# 		mytemp = ''
# 		filename = 'w1_slave'
# 		f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
# 		line = f.readline() # read 1st line
# 		crc = line.rsplit(' ',1)
# 		crc = crc[1].replace('\n', '')
# 		if crc=='YES':
# 			line = f.readline() # read 2nd line
# 			mytemp = line.rsplit('t=',1)
# 		else:
# 			mytemp = 99999
# 		f.close()
# 		return int(mytemp[1])
# 	except:
# 		return 99999
#
# if __name__ == '__main__':
# 	for i in range(1000):
# 		id2='28-0000076aa408'
# 		id1='28-0000076bb328'
# 		print "Temp1: {0:.3f}, Temp2: {1:.3f}".format(gettemp(id1)/float(1000), gettemp(id2)/float(1000))
# 		time.sleep(2)

##############################

temp_sensor_a = "/sys/bus/w1/devices/{}/w1_slave".format(SENSOR_A)
temp_sensor_b = "/sys/bus/w1/devices/{}/w1_slave".format(SENSOR_B)

def read_temp_raw():
	f = open(temp_sensor_b, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1].strip()[equals_pos+2:]
		temp = float(temp_string) / 1000
		return temp

while True:
	time.sleep(1)
	print read_temp()
