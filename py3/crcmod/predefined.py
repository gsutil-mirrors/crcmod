#-----------------------------------------------------------------------------
# Copyright (c) 2010 Craig McQueen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#-----------------------------------------------------------------------------
'''
crcmod.predefined defines some well-known CRC algorithms.

To use it, e.g.:
    import crcmod.predefined
    
    crc32 = crcmod.predefined.PredefinedCrc("crc-32")

crcmod.predefined.Crc is an alias for crcmod.predefined.PredefinedCrc
But if doing 'from crc.predefined import *', only PredefinedCrc is imported.
'''

# local imports
import crcmod

__all__ = [ 'PredefinedCrc' ]

REVERSE = True
NON_REVERSE = False

_crc_definitions_table = [
#       Name                Identifier-name,    Poly            Reverse         Init-value      XOR-out     Check
    [   'crc-8',            'Crc8',             0x107,          NON_REVERSE,    0x00,           0x00,       0xF4,       ],
    [   'crc-16',           'Crc16',            0x18005,        REVERSE,        0x0000,         0x0000,     0xBB3D,     ],
    [   'crc-16-usb',       'Crc16Usb',         0x18005,        REVERSE,        0xFFFF,         0xFFFF,     0xB4C8,     ],
    [   'x-25',             'CrcX25',           0x11021,        REVERSE,        0xFFFF,         0xFFFF,     0x906E,     ],
    [   'kermit',           'CrcKermit',        0x11021,        REVERSE,        0x0000,         0x0000,     0x2189,     ],
    [   'crc-ccitt-false',  'CrcCcittFalse',    0x11021,        NON_REVERSE,    0xFFFF,         0x0000,     0x29B1,     ],
    [   'crc-ccitt',        'CrcCcitt',         0x11021,        NON_REVERSE,    0x1D0F,         0x0000,     0xE5CC,     ],
    [   'crc-32',           'Crc32',            0x104c11db7,    REVERSE,        0xFFFFFFFF,     0xFFFFFFFF, 0xCBF43926, ],
    [   'crc-32c',          'Crc32C',           0x11edc6f41,    REVERSE,        0xFFFFFFFF,     0xFFFFFFFF, 0xE3069283, ],
    [   'crc-32-mpeg',      'Crc32Mpeg',        0x104c11db7,    NON_REVERSE,    0xFFFFFFFF,     0x00000000, 0x0376E6E7, ],

# 64-bit
#       Name                Identifier-name,    Poly                    Reverse         Init-value          XOR-out             Check
    [   'crc-64-jones',     'Crc64Jones',       0x1ad93d23594c935a9,    REVERSE,        0x0000000000000000, 0x0000000000000000, 0xE9C6D914C4B8D9CA, ],
]


def simplify_name(name):
    """
    Reduce CRC definition name to a simplified form:
        * lowercase
        * dashes removed
        * spaces removed
        * any initial "CRC" string removed
    """
    name = name.lower()
    name = name.replace('-', '')
    name = name.replace(' ', '')
    if name.startswith('crc'):
        name = name[len('crc'):]
    return name


_crc_definitions_by_name = {}
_crc_definitions_by_identifier = {}
_crc_definitions = []

_crc_table_headings = [ 'name', 'identifier', 'poly', 'reverse', 'init', 'xor_out', 'check' ]

for table_entry in _crc_definitions_table:
    crc_definition = dict(zip(_crc_table_headings, table_entry))
    _crc_definitions.append(crc_definition)
    name = simplify_name(table_entry[0])
    if name in _crc_definitions_by_name:
        raise Exception("Duplicate entry for '{0}' in CRC table".format(name))
    _crc_definitions_by_name[simplify_name(table_entry[0])] = crc_definition
    _crc_definitions_by_identifier[table_entry[1]] = crc_definition


class PredefinedCrc(crcmod.Crc):
    def __init__(self, crc_name):
        definition = _crc_definitions_by_name.get(simplify_name(crc_name), None)
        if not definition:
            definition = _crc_definitions_by_identifier.get(crc_name, None)
        if not definition:
            raise KeyError("Unkown CRC name '{0}'".format(crc_name))
        super().__init__(poly=definition['poly'], initCrc=definition['init'], rev=definition['reverse'], xorOut=definition['xor_out'])


# crcmod.predefined.Crc is an alias for crcmod.predefined.PredefinedCrc
Crc = PredefinedCrc
