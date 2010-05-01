
import imp
import os
import sys

if sys.version_info[0] == 2:
    version_dir = 'py2'
elif sys.version_info[0] == 3:
    version_dir = 'py3'

test_file_name = os.path.join(
    os.path.dirname(__file__),
    '..',
    version_dir,
    'test',
    'test_crcmod.py'
)

imp.load_source("test_crcmod", test_file_name)
