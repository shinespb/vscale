#!/usr/bin/env python
from distutils.core import setup
 
setup(
    name='vscalib',
    version='0.0.1',
    packages=['vscale'],
    license='MIT',
    description='Library for Vscale.io API!',
    long_description=open('README.md').read(),
    author='Igor Shestakov',
    author_email='shinespb@gmail.com',
    url="https://github.com/shinespb/vscale",
    install_requires=["requests >= 1.0.4"],
)