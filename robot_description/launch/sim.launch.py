import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    
    pkg_name = 'robot_description' 
    file_subpath = 'urdf/Coint5_r2.urdf'

    urdf_file = os.path.join(get_package_share_directory(pkg_name), file_subpath)
    # pkg_path = get_package_share_directory(pkg_name)
    # install_dir = os.path.dirname(pkg_path)

    # gz_resource_path = SetEnvironmentVariable(
    #     name='GZ_SIM_RESOURCE_PATH',
    #     value=[
    #         install_dir, 
    #         ":", 
    #         os.environ.get('GZ_SIM_RESOURCE_PATH', '') # Varsa eski yolları da koru
    #     ]
    # )

    # gazebo = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         [os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]
    #     ),
    #     launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    # )

    with open(urdf_file, 'r') as infp:
        robot_description_raw = infp.read()

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}]
    )

    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # spawn_entity = Node(
    #     package='ros_gz_sim',
    #     executable='create',
    #     arguments=['-topic', 'robot_description', '-name', 'cobot', '-z', '0.0'],
    #     output='screen'
    # )

    rviz_config_file = os.path.join(get_package_share_directory(pkg_name), 'config', 'rviz.rviz')
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher_gui,
        node_rviz
    ])