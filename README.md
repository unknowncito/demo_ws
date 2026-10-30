demo_ws.

ROS workspace for controlling a robot over WebSocket and serial.

Flow
ws_server.py  →  ws_cmd_vel.py  →  /cmd_vel  →  cmd_vel_bridge.py  →  /control  →  Teensy (serial)

Scripts (src/scripts/)

ws_server.py
  Keyboard controller.
  Sends JSON velocity commands over WebSocket.
  Uses WASD keys:
    W = forward
    S = backward
    A = left
    D = right
    X = stop
    Q = quit

ws_cmd_vel.py
  ROS node.
  Connects to the WebSocket server and publishes incoming commands to /cmd_vel as a geometry_msgs/Twist.

cmd_vel_bridge.py
  ROS node.
  Subscribes to /cmd_vel.
  Converts commands to steering and throttle values.
  Publishes the result to /control as a Float32MultiArray for the Teensy.

Launch

roslaunch source bringup.launch

  Starts:
    - rosserial_python serial node for the Teensy
    - cmd_vel_bridge.py
    - ws_cmd_vel.py

  Serial setup:
    port: /dev/teensy
    baud: 57600

Topics

  /cmd_vel   type: geometry_msgs/Twist
  /control   type: std_msgs/Float32MultiArray

Dependencies
  rospy
  geometry_msgs
  std_msgs
  rosserial_python

@copilot 

Important
  The WebSocket URL is configured in the launch file and may differ from the default value used by ws_server.py.
  Check that the WebSocket endpoint matches the actual server you are connecting to.
  
Manual debugging
  thon3 src/scripts/ws_server.py
  python3 src/scripts/ws_cmd_vel.py
  python3 src/scripts/cmd_vel_bridge.pypy
