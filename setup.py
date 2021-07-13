# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def getRequirements(filename):
  return [req.strip()
          for req
          in open(filename).readlines()
          ]


setup(
  name="guardian_core",
  version="0.1.0",
  description="Tips Arena Core",
  packages=find_packages(),
  include_package_data=True,
  install_requires=getRequirements("requirements.txt"),
  extras_require={
    "dev": [getRequirements("requirements-dev.txt")]
  })