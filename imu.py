import time, math
from adafruit_extended_bus import ExtendedI2C as I2C
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_GAME_ROTATION_VECTOR

i2c = I2C(3)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR)

# Yaw determines our car's heading here. Function returns angle between -pi to +pi and converts to deg
def yaw_degrees(q):
	x, y, z, w = q # library returns (i, j, k, real), and q is our axis of rotation as a vector
	return math.degrees(math.atan2(2 * (w*z + x*y), 1-2*(y*y + z*z)))
	# Performing arctangent operation: arctan(sideways / forward)

while True:
	time.sleep(0.1)
	output = yaw_degrees(bno.game_quaternion)
	# x, y, z = bno.gyro
	# print("X: {} Y: {} Z: {}".format(x, y, z))
	print(str(output) + " deg")
