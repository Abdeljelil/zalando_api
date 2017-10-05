#!/usr/bin/env python

from setuptools import find_packages, setup

module_name = "zalando_api"

setup(
    name=module_name,
    version="0.0.1",
    description='',
    long_description='''
''',
    keywords='python zalando_api API RESTFUL postgresql asyncio',
    author='Mohamed abdeljelil',
    url='',
    license='',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],

    use_2to3=True,
    extras_require={
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
