import numpy as np
import math
BAD_X = 10
BAD_Y = -5
TRANS_X = BAD_X - 0#msg.pose.pose.position.x
TRANS_Y = BAD_Y - 0#msg.pose.pose.position.y
print([TRANS_X, TRANS_Y])
if (TRANS_X > 0 and TRANS_Y > 0):
    angle = np.arctan(TRANS_Y/TRANS_X)
    print("1: %f" % (angle*180/math.pi))
elif (TRANS_X < 0 and TRANS_Y > 0):
    angle = math.pi+np.arctan(TRANS_Y/TRANS_X)
    print("2: %f" % (angle*180/math.pi))
elif (TRANS_X < 0 and TRANS_Y < 0):
    angle = math.pi+np.arctan(TRANS_Y/TRANS_X)
    print("3: %f" % (angle*180/math.pi))
elif (TRANS_X > 0 and TRANS_Y < 0):
    angle = 2*math.pi+np.arctan(TRANS_Y/TRANS_X)
    print("4: %f" % (angle*180/math.pi))
