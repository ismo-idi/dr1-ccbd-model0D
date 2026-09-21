"""Rendering-only world. No run flag, physics system or control bridge."""
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, RegisterEventHandler, EmitEvent
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def start(context):
    desc = Path(get_package_share_directory('um6p_campus_description'))
    bringup = Path(get_package_share_directory('um6p_campus_bringup'))
    view = LaunchConfiguration('view').perform(context)
    gui = LaunchConfiguration('gui').perform(context).lower() == 'true'
    command = ['gz', 'sim', '-v', '3', str(desc / 'worlds/campus.sdf')]
    if gui:
        command += ['--gui-config', str(bringup / 'config' / ('overview.config' if view == 'overview' else 'gui.config'))]
    else:
        command += ['-s']
    gazebo = ExecuteProcess(cmd=command, output='screen',
        additional_env={'GZ_SIM_RESOURCE_PATH': str(desc / 'models'),
                        'GZ_SIM_SERVER_CONFIG_PATH': str(bringup / 'config/server.config')})
    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
        name='campus_evidence_bridge', output='screen',
        parameters=[{'config_file': str(bringup / 'config/bridge.yaml')}])
    return [gazebo, bridge, RegisterEventHandler(OnProcessExit(
        target_action=gazebo, on_exit=[EmitEvent(event=Shutdown(reason='Gazebo exited'))]))]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument('view', default_value='courtyard', choices=['courtyard', 'overview']),
        OpaqueFunction(function=start)])
