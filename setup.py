from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyisql',
    version='0.1.0',
    description='Python wrapper for Sybase ISQL command line tool.  Returns resultsets in Pandas DataFrame.',
    long_description=long_description,
    url='https://github.com/IrekRybark/pyisql',
    author='Irek Rybark',
    author_email='irek@rybark.com',
    license='MIT',
    classifiers=[ # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testint',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],    
    packages=['pyisql'],

    install_requires=['pandas', 'configparser'],

    package_data = {
        'pyisql': [
            'examples/*',
        ],
    },
)
