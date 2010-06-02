#!/usr/bin/env python

from setuptools import setup, find_packages
 
setup (
    name='wsgi-apphosting',
    version='0.1',
    description='WSGI application hosting server',
    author='Shinya Okano',
    author_email='tokibito@gmail.com',
    url='http://bitbucket.org/tokibito/wsgi-apphosting/',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=["apphosting"],
    test_suite="tests",
    zip_safe=True,
)
