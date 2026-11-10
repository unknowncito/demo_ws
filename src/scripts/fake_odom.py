#!/usr/bin/env python3

import math

import rospy
import tf
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


rospy.init_node("fake_odom")

odom_pub = rospy.Publisher("/odom", Odometry, queue_size=10)
tf_broadcaster = tf.TransformBroadcaster()

x = 0.0
y = 0.0
heading = 0.0
last_time = None


def cmd_vel_callback(msg):
    global x, y, heading, last_time

    current_time = rospy.Time.now()
    if last_time is not None:
        dt = (current_time - last_time).to_sec()
        if dt > 0.0:
            v = msg.linear.x
            w = msg.angular.z
            x += v * math.cos(heading) * dt
            y += v * math.sin(heading) * dt
            heading += w * dt

    last_time = current_time

    orientation = tf.transformations.quaternion_from_euler(0.0, 0.0, heading)
    ## odom represetion ros wants, by copilot
    
    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"
    odom.child_frame_id = "base_link"
    odom.pose.pose.position.x = x
    odom.pose.pose.position.y = y
    odom.pose.pose.orientation.x = orientation[0]
    odom.pose.pose.orientation.y = orientation[1]
    odom.pose.pose.orientation.z = orientation[2]
    odom.pose.pose.orientation.w = orientation[3]
    odom.twist.twist.linear.x = msg.linear.x
    odom.twist.twist.angular.z = msg.angular.z
    odom_pub.publish(odom)

    tf_broadcaster.sendTransform(
        (x, y, 0.0),
        orientation,
        current_time,
        "base_link",
        "odom",
    )


rospy.Subscriber("/cmd_vel", Twist, cmd_vel_callback)
rospy.spin()

