# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.text') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='LWOI-AMP',
    version='0.1.0',
    description='Layer-wise Optical Inspection of Additively Manufactured Parts',
    long_description=readme,
    author='Alexander-Lisenko',
    url='https://github.com/20alexl/ME_G5',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)