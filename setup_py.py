from distutils.core import setup
import sys

if sys.version_info[0] == 2:
    base_dir = 'py2'
elif sys.version_info[0] == 3:
    base_dir = 'py3'

setup(
name='crcmod',
version='1.6.1',
description='CRC Generator',
author='Ray Buvel',
author_email='rlbuvel@gmail.com',
url='http://crcmod.sourceforge.net/',
packages=['crcmod'],
package_dir={
    'crcmod' : base_dir + '/crcmod',
},

)
