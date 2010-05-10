#-----------------------------------------------------------------------------
# Copyright (c) 2010  Raymond L. Buvel
# Copyright (c) 2010  Craig McQueen
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
'''Unit tests for crcmod functionality'''


import unittest

from crcmod import mkCrcFun, Crc
from crcmod import _usingExtension
from predefined import PredefinedCrc
from predefined import mkPredefinedCrcFun
from predefined import _crc_definitions as _predefined_crc_definitions


#-----------------------------------------------------------------------------
# This polynomial was chosen because it is the product of two irreducible
# polynomials.
# g8 = (x^7+x+1)*(x+1)
g8 = 0x185

#-----------------------------------------------------------------------------
# The following reproduces all of the entries in the Numerical Recipes table.
# This is the standard CCITT polynomial.
g16 = 0x11021

#-----------------------------------------------------------------------------
g24 = 0x15D6DCB

#-----------------------------------------------------------------------------
# This is the standard AUTODIN-II polynomial which appears to be used in a
# wide variety of standards and applications.
g32 = 0x104C11DB7


class KnownAnswerTests(unittest.TestCase):
    known_answers = [
        [ mkCrcFun(g8,0,0),             0xFE,           0x9D        ],
        [ mkCrcFun(g8,-1,1),            0x4F,           0x9B        ],
        [ mkCrcFun(g8,0,1),             0xFE,           0x62        ],
        [ mkCrcFun(g16,0,0),            0x1A71,         0xE556      ],
        [ mkCrcFun(g16,-1,1),           0x1B26,         0xF56E      ],
        [ mkCrcFun(g16,0,1),            0x14A1,         0xC28D      ],
        [ mkCrcFun(g24,0,0),            0xBCC49D,       0xC4B507    ],
        [ mkCrcFun(g24,-1,1),           0x59BD0E,       0x0AAA37    ],
        [ mkCrcFun(g24,0,1),            0xD52B0F,       0x1523AB    ],
        [ mkCrcFun(g32,0,0),            0x6B93DDDB,     0x12DCA0F4  ],
        [ mkCrcFun(g32,0xFFFFFFFFL,1),  0x41FB859FL,    0xF7B400A7L ],
        [ mkCrcFun(g32,0,1),            0x6C0695EDL,    0xC1A40EE5L ],        
    ]

    def test_known_answers(self):
        msg = 'CatMouse987654321'
        for crcfun, v0, v1 in self.known_answers:            self.assertEqual(crcfun('T'), v0)            self.assertEqual(crcfun(msg), v1)            self.assertEqual(crcfun('',0), 0)            self.assertEqual(crcfun(msg[4:], crcfun(msg[:4])), v1)            self.assertEqual(crcfun(msg[-1], crcfun(msg[:-1])), v1)
def runtests():    print "Using extension:", _usingExtension
    unittest.main()if __name__ == '__main__':
    runtests()