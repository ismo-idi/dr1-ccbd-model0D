#!/usr/bin/env bash
set -eo pipefail
cat /etc/os-release
uname -m
df -h .
source /opt/ros/jazzy/setup.bash
command -v ros2 gz colcon
gz sim --versions
ros2 pkg prefix ros_gz_bridge
python3 -c 'import rclpy; print("rclpy: available")'
dpkg-query -W -f='${Package}\t${Version}\n' ros-jazzy-ros-gz \
  ros-jazzy-ros-gz-bridge ros-jazzy-gz-sim-vendor python3-colcon-common-extensions
