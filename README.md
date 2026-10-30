demo_ws.

Chain
ws_server.py  →  ws_cmd_vel.py  →  cmd_vel_bridge.py  →  Teensy (serial)

Scripts (src/scripts/)

ws_server.py
  Sends velocity commands over WebSocket at 10 Hz.
  Not a ROS node. Standalone Python.

ws_cmd_vel.py
  Receives WebSocket JSON, publishes to /cmd_vel as a Twist message.
  ROS node.

cmd_vel_bridge.py
  Subscribes to /cmd_vel, sends speed and steering to the Teensy over serial.
  ROS node.

Topics
  /cmd_vel   { tye : geometry_msgs/Twist   
  published by: ws_cmd_vel subscriber by : cmd_vel_bridge }


dependencies : rospy , geometry_msgs, std_msgs

Running
  Terminal 1: python3 src/scripts/ws_server.py
  Terminal 2: python3 src/scripts/ws_cmd_vel.py
  Terminal 3: python3 src/scripts/cmd_vel_bridge.py
