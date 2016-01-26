import smbus
import mraa 
import time 
import math
import numpy as np
import IMU
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
Apwm=Bpwm=Cpwm=Dpwm=Adir=Bdir=Cdir=Ddir=mode=0 
output = [Apwm,Bpwm,Cpwm,Dpwm,Adir,Bdir,Cdir,Ddir,mode] 
Pin = [14,20,0,21,36,48,47,33,46] #PWM for GP13,GP12,GP182,GP183 Gpio for GP14,GP15,GP49,GP48,GP47

for x in xrange(0,4):
	output[x] = mraa.Pwm(Pin[x])
	output[x].period_us(700)
	output[x].enable(True)
	print x, output[x]
for x in xrange(4,9):
	output[x] = mraa.Gpio(Pin[x])
	output[x].dir(mraa.DIR_OUT)
	print x,output[x]

output[8].write(1) #Set Mode to high

def ramp():
        for x in np.arange(0,1,.05):
                output[0].write(x)
                output[1].write(x)
                output[2].write(x)
                output[3].write(x)
                time.sleep(.1)
        for x in np.arange(1,0,.05):
                output[0].write(x)
                output[1].write(x)
                output[2].write(x)
                output[3].write(x)
                time.sleep(.1)
        for x in xrange(4,8):
                output[x].write(0)
        for x in np.arange(0,1,.05):
                output[0].write(x)
                output[1].write(x)
                output[2].write(x)
                output[3].write(x)
                time.sleep(.1)
        for x in np.arange(1,0,.05):
                output[0].write(x)
                output[1].write(x)
                output[2].write(x)
                output[3].write(x)
                time.sleep(.1)

while True:
        output[Adir].write(1)
        output[Bdir].write(1)
        output[Cdir].write(0)
        output[Ddir].write(0)
        ramp()
        output[Adir].write(1)
        output[Bdir].write(1)
        output[Cdir].write(0)
        output[Ddir].write(0)
        ramp()
        output[Adir].write(1)
        output[Bdir].write(0)
        output[Cdir].write(1)
        output[Ddir].write(0)
        ramp()
##        a = time.time()
##        [ACCx,ACCy,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz] = IMU.read()
##        
##        
##        AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
##        AccYangle =  (math.atan2(ACCz,ACCx)+M_PI/2)*RAD_TO_DEG	
##
##        #Calculate heading
##        heading = 180 * math.atan2(MAGy,MAGx)/M_PI
##
##        if heading < 0:
##                heading += 360
##        
##        b = time.time()
##        LoopTime = b - a
        
