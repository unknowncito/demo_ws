# demo_ws

ROS catkin workspace for a simple robot control bridge that connects WebSocket commands to a Teensy/serial controller.

## Overview

This workspace currently implements a small ROS pipeline for sending movement commands from a WebSocket source into a physical robot controller:

`WebSocket input -> ws_cmd_vel.py -> /cmd_vel -> cmd_vel_bridge.py -> /control -> Teensy via serial`

The current setup is coordinated by `launch/bringup.launch` and the Python scripts under `src/scripts/`.

## Repository structure

- `launch/bringup.launch` - starts the serial node and the control bridge nodes
- `src/CMakeLists.txt` - catkin top-level CMake entry point
- `src/package.xml` - ROS package metadata and dependencies
- `src/scripts/ws_server.py` - local keyboard-based client for generating `cmd_vel` messages over WebSocket
- `src/scripts/ws_cmd_vel.py` - subscribes to the WebSocket and republishes messages as `/cmd_vel`
- `src/scripts/cmd_vel_bridge.py` - ROS node that listens to `/cmd_vel` and converts it to a normalized `/control` array for the Teensy

## Current runtime behavior

`launch/bringup.launch` starts:

1. `rosserial_python` connected to the Teensy on `/dev/teensy` at 57600 baud
2. `cmd_vel_bridge.py` as a ROS node
3. `ws_cmd_vel.py` as a ROS node

This means the robot stack is expected to receive commands from a WebSocket source and translate them into a serial control signal for the microcontroller.

## Message flow

### 1) WebSocket input

The JSON payload expected by `ws_cmd_vel.py` is shaped like:

```json
{
  "type": "cmd_vel",
  "data": {
    "linear": 0.5,
    "angular": 0.0
  }
}
```

`ws_cmd_vel.py` parses that payload and republishes it as a `geometry_msgs/Twist` on the `/cmd_vel` topic.

### 2) ROS `/cmd_vel` topic

`cmd_vel_bridge.py` subscribes to `/cmd_vel` and converts the incoming twist values into a compact `std_msgs/Float32MultiArray` published on `/control`.

The bridge also includes a steering deadzone to keep the wheel centered when the user releases the steering input. In other words:

- `linear.x` is mapped into throttle output
- `angular.z` is mapped into steering output
- small near-zero steering values are treated as zero

## Local keyboard test utility

`src/scripts/ws_server.py` is a lightweight manual test tool. It reads WASD keyboard input and sends JSON messages over WebSocket to a remote/local control server.

Available keys:

- `W` = forward
- `S` = backward
- `A` = left
- `D` = right
- `X` = stop
- `Q` = quit

This script is useful for testing the command pipeline without requiring a full external controller.

## Build and run

From the workspace root:

```bash
cd demo_ws
catkin_make
source devel/setup.bash
```

Then to launch the robot bridge:

```bash
roslaunch launch/bringup.launch
```

For manual keyboard testing:

```bash
python3 src/scripts/ws_server.py
```

## Dependencies

The project depends on the standard ROS stack plus:

- `rospy`
- `geometry_msgs`
- `std_msgs`
- `numpy`
- `websocket-client`
- `rosserial_python`

## Notes

The WebSocket endpoint is currently being updated/used across the scripts. In the current code:

- `launch/bringup.launch` specifies a WebSocket URL of `ws://10.42.0.99:9090`
- `ws_cmd_vel.py` is still hardcoded to `ws://localhost:8765`

This means the final network address may need to be aligned once the remote server endpoint is finalized.

## Summary

This workspace is a lightweight ROS bridge for robot teleop: it turns WebSocket inputs into ROS commands, then converts ROS velocity commands into a Teensy-friendly control array over serial.
