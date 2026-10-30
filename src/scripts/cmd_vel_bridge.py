#!/usr/bin/env python3


import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
import numpy as np

## by Teyema in gh
##cmd_vel to  thru the conFloat32MultiArray thru control topic



# Steering deadzone: angular.z values below this threshold snap to 0.
# Fixes wheels not returning to centre when controller releases the stick
# (residual angular.z keeps servo slightly off-centre without this).
STEERING_DEADZONE = 0.03

def cmd_vel_callback(msg):
    out = Float32MultiArray(data=[0.0, 0.0, -1.0])

    # Steering with deadzone
    angular = msg.angular.z
    if abs(angular) < STEERING_DEADZONE:
        angular = 0.0
    out.data[1] = -np.clip(angular, -1.0, 1.0)

    # Throttle — output is normalised (-1 to 1), not m/s.
    # Min/max speed in m/s is enforced via TebLocalPlannerROS max_vel_x
    # and min_vel_x in planner.yaml, not here.
    if msg.linear.x > 0.001:
        out.data[0] = np.clip(msg.linear.x, 0.1, 1.0)
    elif msg.linear.x < -0.001:
        out.data[0] = np.clip(msg.linear.x, -1.0, -0.1)
    else:
        out.data[0] = 0.0

    pub.publish(out)

rospy.init_node('cmd_vel_bridge')
pub = rospy.Publisher('/control', Float32MultiArray, queue_size=10)
rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback)
rospy.spin()
