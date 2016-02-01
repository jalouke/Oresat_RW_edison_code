
import smbus
import time
import math
from LSM9DS0 import *

bus = smbus.SMBus(1)

LA_So = .000732 # g/LSB (16g)
M_GN = 0.48 # mgauss/LSB (12 gauss)
G_So = 0.07 # dps/LSB (2000dps)
GYRx_offset = -0.24 
GYRy_offset = -6.72
GYRz_offset = -0.24
timestart = time.time()

def writeACC(register,value):
        bus.write_byte_data(ACC_ADDRESS , register, value)
        return -1

def writeMAG(register,value):
        bus.write_byte_data(MAG_ADDRESS, register, value)
        return -1

def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1

def readACCx():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536

def readACCy():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536

def readACCz():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536

def readMAGx():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536

def readMAGy():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536

def readGYRx():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536
  
def readGYRy():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

def readGYRz():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

	
#initialise the accelerometer
writeACC(CTRL_REG1_XM, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
writeACC(CTRL_REG2_XM, 0b00100000) #+/- 16G full scale

#initialise the magnetometer
writeMAG(CTRL_REG5_XM, 0b11110000) #Temp enable, M data rate = 50Hz
writeMAG(CTRL_REG6_XM, 0b01100000) #+/-12gauss
writeMAG(CTRL_REG7_XM, 0b00000000) #Continuous-conversion mode

#initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b00001111) #Normal power mode, all axes enabled
writeGRY(CTRL_REG4_G, 0b00110000) #Continuos update, 2000 dps full scale

GYRx_max=GYRy_max=GYRz_max=0
GYRx_min=GYRy_min=GYRz_min=0
print "calibrating 3..."
time.sleep(1)
print "calibrating 2..."
time.sleep(1)
print "calibrating 1..."
time.sleep(1)
start=time.time()
timer=0
while timer<10:
	GYRx = readGYRx()
	GYRy = readGYRy()
	GYRz = readGYRz()
	if GYRx > GYRx_max : GYRx_max = GYRx 
	if GYRx < GYRx_min : GYRx_min = GYRx
	if GYRy > GYRy_max : GYRy_max = GYRy
	if GYRy < GYRy_min : GYRy_min = GYRy
	if GYRz > GYRz_max : GYRz_max = GYRz
	if GYRz < GYRz_min : GYRz_min = GYRz
	timer=time.time()-start
GYRx_bias  = (GYRx_max + GYRx_min)/2
GYRy_bias  = (GYRy_max + GYRy_min)/2
GYRz_bias  = (GYRz_max + GYRz_min)/2
GYRx_scalea = (GYRx_max - GYRx_min)/2
GYRy_scalea = (GYRy_max - GYRy_min)/2
GYRz_scalea = (GYRz_max - GYRz_min)/2
avg_scale = (GYRx_scalea+GYRy_scalea+GYRz_scalea)/3
GYRx_scale = avg_scale/GYRx_scalea
GYRy_scale = avg_scale/GYRy_scalea
GYRz_scale = avg_scale/GYRz_scalea
print "GYRx bias = %3.4f, GYRx scale = %3.4f" % (GYRx_bias,GYRx_scale)
print "GYRy bias = %3.4f, GYRy scale = %3.4f" % (GYRy_bias,GYRy_scale)
print "GYRz bias = %3.4f, GYRz scale = %3.4f" % (GYRz_bias,GYRz_scale)
