"""Demo 2; explicitly starts paused."""
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    shared=Path(get_package_share_directory('um6p_demo_core'))/'launch/demo.launch.py'
    return LaunchDescription([
        DeclareLaunchArgument('gui',default_value='true',choices=['true','false']),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(shared)),
            launch_arguments={'scenario_package':'um6p_demo_2',
                'gui':LaunchConfiguration('gui')}.items())])
