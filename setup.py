from distutils.core import setup
from distutils.extension import Extension
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

ext_modules=[ 
    Extension('crcmod._crcfunext', [ base_dir + '/src/_crcfunext.c', ],
    ),
],

long_description=open('README').read(),

license="MIT",
classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: C++',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Communications',
    'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Utilities',
],
)
