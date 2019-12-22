import setuptools
from distutils.core import setup

setup(name='aoc-intcpu',
      version='1.0.2',
      description='IntCode Emulator from AoC 2019',
      author='Thomas Hiscock',
      author_email='thomashk000@gmail.com',
      setup_requires=['wheel'],
      packages=['intcpu'],
      package_data={'intcpu': ['*.so']},
      include_package_data=True)
