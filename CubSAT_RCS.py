import smbus
import time
import math
import mraa
from IMU import IMU_read
Apwm=Bpwm=Cpwm=Dpwm=Adir=Bdir=Cdir=Ddir=mode=0
output = [Apwm,Bpwm,Cpwm,Dpwm,Adir,Bdir,Cdir,Ddir,mode]
Pin = [14,20,0,21,36,48,47,33,46] #PWM for GP13,GP12,GP182,GP183 Gpio for GP14,GP15,GP49,GP48,GP47

for x in xrange(0,3):
	output[x] = mraa.Pwm(Pin[x])
	output[x].period_us(700)
	output[x].enable(True)
	print output[x]
for x in xrange(4,8):
	output[x] = mraa.Gpio(Pin[x])
	output[x].dir(mraa.DIR_OUT)
	print output[x]
	
PWM_A = 0.0
PWM_B = 0.0
PWM_C = 0.0
PWM_D = 0.0



