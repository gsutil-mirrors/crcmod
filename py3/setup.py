from distutils.core import setup
from distutils.extension import Extension

setup(
name='crcmod',
version='1.6',
description='CRC Generator',
author='Ray Buvel',
author_email='rlbuvel@gmail.com',
url='http://crcmod.sourceforge.net/',
packages=['crcmod'],

ext_modules=[ 
    Extension('crcmod._crcfunext', ['src/_crcfunext.c', ],
    ),
],
)
