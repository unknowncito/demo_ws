cmake_minimum_required(VERSION 3.0.2)
project(source)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  rospy
  std_msgs
  tf
)

catkin_package(
  CATKIN_DEPENDS geometry_msgs nav_msgs rospy std_msgs tf
)

catkin_install_python(PROGRAMS
  ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/cmd_vel_bridge.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/fake_odom.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/ws_cmd_vel.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../scripts/ws_server.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)
