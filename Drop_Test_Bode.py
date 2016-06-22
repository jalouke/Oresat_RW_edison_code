##This code is written to give the CubeSAT a constant angular velocity about the z-axis##

#"System Management Bus", turning on and off?
import smbus
#allows easy interface w/ I/O pins on Edison board
import mraa
#time module
import time
#math module
import math
#to be able to use large arrays and matrices
import numpy as np
#?
import IMU
#to process command line arguments
import sys

#########################################################
#Initializing Variables

#frequency of input response in Hz
Frequency = 1
#motor velocities initially set to zero
A_motor_velocity=B_motor_velocity=C_motor_velocity=D_motor_velocity=0
#x,y,z velocities initially set to zero
X_velocity=Y_velocity=Z_velocity=0
#initialize outputs equal to zero
A=B=C=D=E=F=G=H=I=0
#define A-I as an array
output = ['A','B','C','D','E','F','G','H','I']
#Edison pins GP13,GP12,GP182,GP183 as PWM
#Edison pins GP14,GP15,GP49,GP46,GP47 as GPIO
Pin = [14,20,0,21,36,48,47,32,46]
pi = 3.1415926
#transformation coefficient #1
c_a = np.sin(45*pi/180)/2
#transformation coefficient #2
c_b = np.sin(45*pi/180)/2
#transformation coefficient #3
c_c = 1/(np.cos(53*pi/180)*4)
#cubesat reference frame to motor reference frame conversion (3x4)
Card_to_Motor = [[c_a,c_b,c_c],[c_a,-c_b,c_c],[-c_a,-c_b,c_c],[-c_a,c_b,c_c]]
#?
phase=0
#time initially equal to zero
t=0

##########################################################

#Enabling Outputs 
for x in xrange(0,4):
	output[x] = mraa.Pwm(Pin[x])
	output[x].period_us(700)
	output[x].enable(True)
	print x, output[x]
for x in xrange(4,9):
	output[x] = mraa.Gpio(Pin[x])
	output[x].dir(mraa.DIR_OUT)
	print x, output[x]
[Apwm,Bpwm,Cpwm,Dpwm,Adir,Bdir,Cdir,Ddir,mode] = output
output[8].write(1) #Set mode pin to high for pwm/direction
print Apwm
###########################################################
def A_motor(A_motor_velocity):
        if A_motor_velocity >= 0:
                 A_motor_dir = 1
                 A_motor_speed = abs(A_motor_velocity)
                 if A_motor_speed > 1:
                         A_motor_speed = 1
        elif A_motor_velocity < 0:
                 A_motor_dir = 0
                 A_motor_speed = abs(A_motor_velocity)
                 if A_motor_speed > 1:
                         A_motor_speed = 1
        Adir.write(A_motor_dir)
        Apwm.write(A_motor_speed)
        print A_motor_dir,A_motor_speed
def B_motor(B_motor_velocity):
        if B_motor_velocity >= 0:
                 B_motor_dir = 1
                 B_motor_speed = abs(B_motor_velocity)
                 if B_motor_speed > 1:
                         B_motor_speed = 1
        elif B_motor_velocity < 0:
                 B_motor_dir = 0
                 B_motor_speed = abs(B_motor_velocity)
                 if B_motor_speed > 1:
                         B_motor_speed = 1
        Bdir.write(B_motor_dir)
        Bpwm.write(B_motor_speed)
def C_motor(C_motor_velocity):
        if C_motor_velocity >= 0:
                 C_motor_dir = 1
                 C_motor_speed = abs(C_motor_velocity)
                 if C_motor_speed > 1:
                         C_motor_speed = 1
        elif C_motor_velocity < 0:
                 C_motor_dir = 0
                 C_motor_speed = abs(C_motor_velocity)
                 if C_motor_speed > 1:
                         C_motor_speed = 1
        Cdir.write(C_motor_dir)
        Cpwm.write(C_motor_speed)
def D_motor(D_motor_velocity):
        if D_motor_velocity >= 0:
                 D_motor_dir = 1
                 D_motor_speed = abs(D_motor_velocity)
                 if D_motor_speed > 1:
                         D_motor_speed = 1
        elif D_motor_velocity < 0:
                 D_motor_dir = 0
                 D_motor_speed = abs(D_motor_velocity)
                 if D_motor_speed > 1:
                         D_motor_speed = 1
        Ddir.write(D_motor_dir)
        Dpwm.write(D_motor_speed)
def shutdown():
        Adir.write(0)
        Bdir.write(0)
        Cdir.write(0)
        Ddir.write(0)
        Apwm.write(0) 
        Bpwm.write(0) 
        Cpwm.write(0) 
        Dpwm.write(0) 
        sys.exit() 
def freq_response(Frequency,timestart):
        t = time.time()-timestart
        Z_velocity = np.sin(Frequency*t*pi*2)
        print t,Z_velocity
        [A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity]=np.dot(Card_to_Motor,[[X_velocity],[Y_velocity],[Z_velocity]])
        return A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity
filename = time.strftime("%Y-%m-%d_%H-%M-%S")
Data = open(('Drop_Test/CubeSat_Drop').__add__(filename).__add__('.csv'), 'a')
Data.write('Time,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz,A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity\n')

while True:
        [ACCx,ACCy,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz] = IMU.read()
        timestart = time.time()
        while ACCz > -.8:
                t = time.time()-timestart
                phase = 2
                [A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity] = freq_response(Frequency,timestart)
                print A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity
                A_motor(A_Motor_velocity)
                B_motor(B_Motor_velocity)
                C_motor(C_Motor_velocity)
                D_motor(D_Motor_velocity)
                print A_Motor_velocity
                Data.write('%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f\n' % (t,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz,A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity))
        if phase == 2 and ACCz <-.8:
                shutdown()
                
