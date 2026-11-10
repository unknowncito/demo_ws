demo_ws

ROS workspace for WebSocket → Teensy control and LD19 testing.

Flow
ws_server.py → ws_cmd_vel.py → /cmd_vel → cmd_vel_bridge.py → /control → Teensy

Build

  cd /root/demo_ws
  catkin_make
  source devel/setup.bash

The ROS package is `source` in `src/source`.

Control

  roslaunch source bringup.launch

Starts the Teensy serial node, command bridge, and WebSocket receiver.
The keyboard sender (`src/scripts/ws_server.py`) is started separately.

Note: `ws_cmd_vel.py` uses `ws://localhost:8765`; it does not read the URL
parameter in `bringup.launch`.

LD19

  roslaunch ldlidar_stl_ros ld19.launch

Publishes `scan` in frame `base_laser` and sets `base_link → base_laser`.
The lidar is not connected yet, so `/scan` has not been verified.

Fake odometry

  rosrun source fake_odom.py

Subscribes to `/cmd_vel`, publishes `/odom`, and broadcasts `odom → base_link`.
This estimates motion from commands; it is for testing, not real robot odometry.
Do not run it with DLIO or another odometry source.

Mapping notes

- Navigation loads `empty_map.yaml`; no gmapping launch is provided.
- DLIO in `rtx_ws/dlio.zip` uses Azure Kinect point-cloud and IMU data.
- DLIO uses `camera_base`; navigation expects `base_link`. These frames need
  to be reconciled before mapping.
- `move_base.launch` passes `range_min` to the LD19 launch, which does not
  declare that argument.
