import numpy as np
pi = 3.14159
c_a = np.sin(45*pi/180)/2 #transformation coefficient #1
c_b = np.sin(45*pi/180)/2 #transformation coefficient #2
c_c = 1/(np.cos(53*pi/180)*4) #transformation coefficient #3
X_velocity=Y_velocity=Z_velocity=1
Card_to_Motor = [[c_a,c_b,c_c],[c_a,-c_b,c_c],[-c_a,-c_b,c_c],[-c_a,c_b,c_c]] #cubesat reference frame to motor reference frame conversion (3x4)
Cardinal_axis = [[X_velocity],[Y_velocity],[Z_velocity]]
[A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity]=np.dot(Card_to_Motor,Cardinal_axis)

print A_Motor_velocity,B_Motor_velocity,C_Motor_velocity,D_Motor_velocity
