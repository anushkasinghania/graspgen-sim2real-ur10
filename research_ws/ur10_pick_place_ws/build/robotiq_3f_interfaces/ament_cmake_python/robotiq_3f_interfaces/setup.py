from setuptools import find_packages
from setuptools import setup

setup(
    name='robotiq_3f_interfaces',
    version='0.0.1',
    packages=find_packages(
        include=('robotiq_3f_interfaces', 'robotiq_3f_interfaces.*')),
)
