import MRAA
import time

x = mraa.i2c(1)
gyro_address = 0x6B
mag_acc_address = 0x1D
x.address(gyro_address)
y.address(mag_acc_address)

def IMU():
    x.address(IMU_address)
    Gyx = np.int16(x.readReg(0x28) | x.readReg(0x29)<<8)
    GyY = np.int16(x.readReg(0x2A) | x.readReg(0x2B)<<8)
    GyZ = np.int16(x.readReg(0x2C) | x.readReg(0x2D)<<8)
    y.address(mag_acc_address)
    MaX = np.int16(y.readReg(0x08) | y.readReg(0x09)<<8)
    MaY = np.int16(y.readReg(0x0A) | y.readReg(0x0B)<<8)
    MaZ = np.int16(y.readReg(0x0C) | y.readReg(0x0D)<<8)
    AcX = np.int16(y.readReg(0x28) | y.readReg(0x29)<<8)
    AcY = np.int16(y.readReg(0x2A) | y.readReg(0x2B)<<8)
    AcZ = np.int16(y.readReg(0x2C) | y.readReg(0x2D)<<8)
    return Gyx, GyY, GyZ, AcX, AcY, AcZ, MaX, MaY, MaZ
    
while True:
    IMU()
    print Gyx, GyY, GyZ, AcX, AcY, AcZ, MaX, MaY, MaZ
