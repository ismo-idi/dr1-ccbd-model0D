"""Separate explicitly enabled kinematic mode. Default starts paused."""
from pathlib import Path
import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, RegisterEventHandler, EmitEvent
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def start(context):
    demo=Path(get_package_share_directory('um6p_demo_core'))
    scenario=Path(get_package_share_directory(LaunchConfiguration('scenario_package').perform(context)))
    desc=Path(get_package_share_directory('um6p_campus_description'))
    bringup=Path(get_package_share_directory('um6p_campus_bringup'))
    gui=LaunchConfiguration('gui').perform(context)=='true'
    command=['gz','sim','-v','3',str(scenario/'worlds/demo.sdf')]
    if gui: command+=['--gui-config',str(demo/'config/gui.config')]
    else: command+=['-s']
    gazebo=ExecuteProcess(cmd=command,output='screen',additional_env={
        'GZ_SIM_RESOURCE_PATH':str(desc/'models'),
        'GZ_SIM_SYSTEM_PLUGIN_PATH':str(Path(get_package_prefix('um6p_demo_core'))/'lib'),
        'GZ_GUI_PLUGIN_PATH':str(Path(get_package_prefix('um6p_demo_core'))/'lib'),
        'GZ_SIM_SERVER_CONFIG_PATH':str(bringup/'config/server.config')})
    bridge=Node(package='ros_gz_bridge',executable='parameter_bridge',name='campus_demo_bridge',
                parameters=[{'config_file':str(demo/'config/bridge.yaml')}],output='screen',
                namespace=os.environ.get('CAMPUS_VERIFY_NAMESPACE',''),
                remappings=[('/campus/demo/state','/'+os.environ['CAMPUS_VERIFY_NAMESPACE']+'/state'),
                            ('/clock','/'+os.environ['CAMPUS_VERIFY_NAMESPACE']+'/clock')]
                    if os.environ.get('CAMPUS_VERIFY_NAMESPACE') else [])
    return [gazebo,bridge,RegisterEventHandler(OnProcessExit(target_action=gazebo,
        on_exit=[EmitEvent(event=Shutdown(reason='Gazebo exited'))]))]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('scenario_package',choices=['um6p_demo_1','um6p_demo_2']),
        DeclareLaunchArgument('gui',default_value='true',choices=['true','false']),
        OpaqueFunction(function=start)])
