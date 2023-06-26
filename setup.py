#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='clean_architecture',
      version='0.0.1',
      description='This package has shared components.',
      author='Dung Phan Quang',
      author_email='phanquangdng@gmail.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      license='LICENSE.txt',
    )