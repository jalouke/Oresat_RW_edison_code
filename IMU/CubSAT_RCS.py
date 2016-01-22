import smbus
import time
import math
import mraa
from IMU import IMU_read
Ain1=Bin1=Cin1=Din1=Ain2=Bin2=Cin2=Din2=0
Motors1 = [Ain1,Bin1,Cin1,Din1]
Motors2 = [Ain2,Bin2,Cin2,Din2]
PWM = [14,20,0,21] #PWM for GP13,GP12,GP102,GP103
Gpio = [45,46,47,36] #Gpio for GP45,GP47,GP49,GP14
for x in xrange(4):
	Motors1[x] = mraa.Pwm(PWM[x])
	Motors1[x].period_us(700)
	Motors1[x].enable(True)
	print Motors1[x]

	Motors2[x] = mraa.Gpio(Gpio[x])
	print Motors2[x]
	Motors2[x].dir(mraa.DIR_OUT)
	
PWM_A = 0.0
PWM_B = 0.0
PWM_C = 0.0
PWM_D = 0.0



