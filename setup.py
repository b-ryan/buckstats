#!/usr/bin/env python
from setuptools import setup, find_packages

pkg_name = 'buckstats'
pkg_version = '0.0.1'

setup(
    name=pkg_name,
    version=pkg_version,
    packages=find_packages(),
    install_requires=[
        'gspread',
        'alembic',
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Restless',
        'requests',
    ],
)
