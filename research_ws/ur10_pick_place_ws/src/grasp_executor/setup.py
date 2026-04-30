from setuptools import find_packages, setup

package_name = 'grasp_executor'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='GraspGen pick-and-place executor node for UR10 + Robotiq 3F',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'grasp_executor_node = grasp_executor.grasp_executor_node:main',
            'graspgen_bridge_node = grasp_executor.graspgen_bridge_node:main',
        ],
    },
)
