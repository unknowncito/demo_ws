#!/usr/bin/env python3
#take websocket cmd and pass it to  bridge.py 
# 10/29/36

import json
import threading
import rospy
import websocket
from geometry_msgs.msg import Twist


rospy.init_node("ws_cmd_vel")
pub = rospy.Publisher("/cmd_vel", Twist, queue_size =1 )
URL = "ws://localhost:8765"

def on_message(ws, message):
    """Handle incoming cmd_vel messages."""
    try:
        #make it into a python dic
        msg = json.loads(message)

        if msg.get("type") != "cmd_vel":
            return

        #instance of twist msg
        cmd = Twist()
        cmd.linear.x = float(msg["data"]["linear"])
        cmd.angular.z = float(msg["data"]["angular"])

        #publish to /cmd_vel
        pub.publish(cmd)

    except (ValueError, KeyError, TypeError) as e:
        rospy.logwarn("Invalid command: %s", e)

def on_open(ws):
    rospy.loginfo("Connected to WebSocket server")

def on_error(ws, error):
    rospy.logerr("WebSocket error: %s", error)

# creates and sets and websocket client
ws = websocket.WebSocketApp(
    URL,
    on_message=on_message,
    on_open=on_open,
    on_error=on_error
)

#thread to run ws
threading.Thread(target=ws.run_forever, daemon=True).start()

# run till shutdown
rospy.spin()
