#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup
import os


README = os.path.join(os.path.dirname(__file__), 'README.rst')
REQUIREMENTS = os.path.join(os.path.dirname(__file__), 'requirements.txt')


if __name__ == "__main__":
    setup(name='batch-tips-arena',
          description='Aplicação execução das rotinas batch.',
          version='1.0',
          long_description=open(README).read(),
          author="First-Up Tech", author_email="devrocks.tech@gmail.com",
          install_requires=open(REQUIREMENTS).readlines(),
          packages=['tipsarena_app'],
          package_dir={"rotinas_batch"},
          entry_points={
              'console_scripts': [
                  'tipsarena_app = Main',
              ]
          },
          zip_safe=False,
          platforms='any',
          include_package_data=True,
          classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'Intended Audience :: Financial and Insurance Industry',
              'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
              'Natural Language :: Portuguese (Brazilian)',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3 :: Only'
          ])
