#import smbus
import time
import math
import sys
import IMU
GYRx_offset=0.821042
GYRy_offset=-1.359071
GYRz_offset=-0.950266
GYRx_tot=GYRy_tot=GYRz_tot=0
count = 0

filename = time.strftime("%Y-%m-%d_%H:%M:%S")
Data = open(('CubeSat_Drop').__add__(filename).__add__('.txt'), 'a')
Data.write('Time,ACCx,ACCy,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz\n')
start_time = time.time()
t=0
while t<25:
        [ACCx,ACCy,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz] = IMU.read()

        print ("\033[1;34;40mAcceleration Values:")
        print ("\033[1;34;40mACCX %5.4f, ACCy %5.4f, ACCz %5.4f" % (ACCx, ACCy, ACCz))
        print ("\033[1;31;40mGyro Values:")
        print ("\033[1;31;40mGYRx %5.2f, GYRy %5.2f, GYRz %5.2f" % (GYRx, GYRy, GYRz))
        print ("\033[1;35;40mMagnetometer values:")
        print ("\033[1;35;40mMAGx %5.2f, MAGy %5.2f, MAGz %5.2f" % (MAGx, MAGy, MAGz))	
        time.sleep(0.1)
	t=time.time()-start_time
	Data.write('%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f\n' % (t,ACCx,ACCy,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz))
	GYRx_tot += GYRx
	GYRy_tot += GYRy
	GYRz_tot += GYRz
	count += 1
Data.close()
GYRx_off = GYRx_tot/count
GYRy_off = GYRy_tot/count
GYRz_off = GYRz_tot/count
print 'GYRx offset = %2.6f, GYRy offset = %2.6f, GYRz offset = %2.6f' % (GYRx_off,GYRy_off,GYRz_off) 
