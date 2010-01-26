#-----------------------------------------------------------------------------
# Test script for crcmod.
#
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

from crcmod import mkCrcFun, Crc
from crcmod.crcmod import _usingExtension
from crcmod.predefined import PredefinedCrc
from crcmod.predefined import mkPredefinedCrcFun
from crcmod.predefined import _crc_definitions as _predefined_crc_definitions

print('_usingExtension', _usingExtension)

#-----------------------------------------------------------------------------
# Test function to verify CRC functions against the test cases listed in
# Numerical Recipes in C.

msg = b'CatMouse987654321'

def checkResult(crc, expected):
    if crc != expected:
        print('Expected: 0x%X, Got: 0x%X' % (expected, crc))
        raise RuntimeError('Test failed')

def test(crcfun, v0, v1):
    checkResult(crcfun(b'T'), v0)
    checkResult(crcfun(msg), v1)
    checkResult(crcfun(b'',0), 0)
    checkResult(crcfun(msg[4:], crcfun(msg[:4])), v1)
    checkResult(crcfun(msg[-1:], crcfun(msg[:-1])), v1)

#-----------------------------------------------------------------------------
# This polynomial was chosen because it is the product of two irreducible
# polynomials.
# g8 = (x^7+x+1)*(x+1)

g8 = 0x185
test(mkCrcFun(g8,0,0),  0xFE, 0x9D)
test(mkCrcFun(g8,-1,1), 0x4F, 0x9B)
test(mkCrcFun(g8,0,1),  0xFE, 0x62)

#-----------------------------------------------------------------------------
# The following reproduces all of the entries in the Numerical Recipes table.
# This is the standard CCITT polynomial.

g16 = 0x11021
test(mkCrcFun(g16,0,0),  0x1A71, 0xE556)
test(mkCrcFun(g16,-1,1), 0x1B26, 0xF56E)
test(mkCrcFun(g16,0,1),  0x14A1, 0xC28D)

#-----------------------------------------------------------------------------
g24 = 0x15D6DCB
test(mkCrcFun(g24,0,0),  0xBCC49D, 0xC4B507)
test(mkCrcFun(g24,-1,1), 0x59BD0E, 0x0AAA37)
test(mkCrcFun(g24,0,1),  0xD52B0F, 0x1523AB)

#-----------------------------------------------------------------------------
# This is the standard AUTODIN-II polynomial which appears to be used in a
# wide variety of standards and applications.

g32 = 0x104C11DB7
test(mkCrcFun(g32,0,0), 0x6B93DDDB, 0x12DCA0F4)
test(mkCrcFun(g32,0xFFFFFFFF,1), 0x41FB859F, 0xF7B400A7)
test(mkCrcFun(g32,0,1), 0x6C0695ED, 0xC1A40EE5)

#-----------------------------------------------------------------------------
# The binascii module has a 32-bit CRC function that is used in a wide range
# of applications including the checksum used in the ZIP file format.  This
# test is to use crcmod to reproduce the same function.

from binascii import crc32

# The following function produces the same result as crc32.
def try32(d, crc=0, fun=mkCrcFun(g32,0,1)):
    return fun(d, crc ^ 0xFFFFFFFF) ^ 0xFFFFFFFF

test(crc32, 0xBE047A60, 0x084BFF58)
test(try32, 0xBE047A60, 0x084BFF58)

#-----------------------------------------------------------------------------
# I was able to locate a couple of 64-bit polynomials on the web.  To make it
# easier to input the representation, define a function that builds a
# polynomial from a list of the bits that need to be turned on.

def polyFromBits(bits):
    p = 0
    for n in bits:
        p = p | (1 << n)
    return p

# The following is from the paper "An Improved 64-bit Cyclic Redundancy Check
# for Protein Sequences" by David T. Jones

g64a = polyFromBits([64, 63, 61, 59, 58, 56, 55, 52, 49, 48, 47, 46, 44, 41,
            37, 36, 34, 32, 31, 28, 26, 23, 22, 19, 16, 13, 12, 10, 9, 6, 4,
            3, 0])

# The following is from Standard ECMA-182 "Data Interchange on 12,7 mm 48-Track
# Magnetic Tape Cartridges -DLT1 Format-", December 1992.

g64b = polyFromBits([64, 62, 57, 55, 54, 53, 52, 47, 46, 45, 40, 39, 38, 37,
            35, 33, 32, 31, 29, 27, 24, 23, 22, 21, 19, 17, 13, 12, 10, 9, 7,
            4, 1, 0])

#-----------------------------------------------------------------------------
# This class is used to check the CRC calculations against a direct
# implementation using polynomial division.

class poly:
    '''Class implementing polynomials over the field of integers mod 2'''
    def __init__(self,p):
        if p < 0: raise ValueError('invalid polynomial')
        self.p = p

    def __int__(self):
        return self.p

    def __eq__(self,other):
        return self.p == other.p

    def __ne__(self,other):
        return self.p != other.p

    def __bool__(self):
        return self.p != 0

    def __neg__(self):
        return self # These polynomials are their own inverse under addition

    def __invert__(self):
        n = max(self.deg() + 1, 1)
        x = (1 << n) - 1
        return poly(self.p ^ x)

    def __add__(self,other):
        return poly(self.p ^ other.p)

    def __sub__(self,other):
        return poly(self.p ^ other.p)

    def __mul__(self,other):
        a = self.p
        b = other.p
        if a == 0 or b == 0: return poly(0)
        x = 0
        while b:
            if b&1:
                x = x ^ a
            a = a<<1
            b = b>>1
        return poly(x)

    def __divmod__(self,other):
        u = self.p
        m = self.deg()
        v = other.p
        n = other.deg()
        if v == 0: raise ZeroDivisionError('polynomial division by zero')
        if n == 0: return (self,poly(0))
        if m < n: return (poly(0),self)
        k = m-n
        a = 1 << m
        v = v << k
        q = 0
        while k > 0:
            if a & u:
                u = u ^ v
                q = q | 1
            q = q << 1
            a = a >> 1
            v = v >> 1
            k -= 1
        if a & u:
            u = u ^ v
            q = q | 1
        return (poly(q),poly(u))

    def __div__(self,other):
        return self.__divmod__(other)[0]

    def __mod__(self,other):
        return self.__divmod__(other)[1]

    def __repr__(self):
        return 'poly(0x%X)' % self.p

    def __str__(self):
        p = self.p
        if p == 0: return '0'
        lst = { 0:[], 1:['1'], 2:['x'], 3:['1','x'] }[p&3]
        p = p>>2
        n = 2
        while p:
            if p&1: lst.append('x^%d' % n)
            p = p>>1
            n += 1
        lst.reverse()
        return '+'.join(lst)

    def deg(self):
        '''return the degree of the polynomial'''
        a = self.p
        if a == 0: return -1
        n = 0
        while a >= 0x10000:
            n += 16
            a = a >> 16
        while a > 1:
            n += 1
            a = a >> 1
        return n

#-----------------------------------------------------------------------------
# The following functions compute the CRC using direct polynomial division.
# These functions are checked against the result of the table driven
# algorithms.

g8p = poly(g8)
x8p = poly(1<<8)
def crc8p(d):
    p = 0
    for i in d:
        p = p*256 + i
    p = poly(p)
    return int(p*x8p%g8p)

g16p = poly(g16)
x16p = poly(1<<16)
def crc16p(d):
    p = 0
    for i in d:
        p = p*256 + i
    p = poly(p)
    return int(p*x16p%g16p)

g24p = poly(g24)
x24p = poly(1<<24)
def crc24p(d):
    p = 0
    for i in d:
        p = p*256 + i
    p = poly(p)
    return int(p*x24p%g24p)

g32p = poly(g32)
x32p = poly(1<<32)
def crc32p(d):
    p = 0
    for i in d:
        p = p*256 + i
    p = poly(p)
    return int(p*x32p%g32p)

g64ap = poly(g64a)
x64p = poly(1<<64)
def crc64ap(d):
    p = 0
    for i in d:
        p = p*256 + i
    p = poly(p)
    return int(p*x64p%g64ap)

g64bp = poly(g64b)
def crc64bp(d):
    p = 0
    for i in d:
        p = p*256 + i
    p = poly(p)
    return int(p*x64p%g64bp)

# Check the CRC calculations against the same calculation done directly with
# polynomial division.

test(mkCrcFun(g8,0,0),  crc8p(b'T'),  crc8p(msg))
test(mkCrcFun(g16,0,0), crc16p(b'T'), crc16p(msg))
test(mkCrcFun(g24,0,0), crc24p(b'T'), crc24p(msg))
test(mkCrcFun(g32,0,0), crc32p(b'T'), crc32p(msg))
test(mkCrcFun(g64a,0,0), crc64ap(b'T'), crc64ap(msg))
test(mkCrcFun(g64b,0,0), crc64bp(b'T'), crc64bp(msg))

#-----------------------------------------------------------------------------
# Verify the methods.

crc = Crc(g32)

str_rep = '''poly = 0x104C11DB7
reverse = True
initCrc  = 0xFFFFFFFF
xorOut   = 0x00000000
crcValue = 0xFFFFFFFF'''
assert str(crc) == str_rep
assert crc.digest() == b'\xff\xff\xff\xff'
assert crc.hexdigest() == 'FFFFFFFF'

crc.update(msg)
assert crc.crcValue == 0xF7B400A7
assert crc.digest() == b'\xf7\xb4\x00\xa7'
assert crc.hexdigest() == 'F7B400A7'

x = crc.copy()
assert x is not crc
str_rep = '''poly = 0x104C11DB7
reverse = True
initCrc  = 0xFFFFFFFF
xorOut   = 0x00000000
crcValue = 0xF7B400A7'''
assert str(crc) == str_rep
assert str(x) == str_rep

# Verify methods when using xorOut

crc = Crc(g32, initCrc=0, xorOut=~0)

str_rep = '''poly = 0x104C11DB7
reverse = True
initCrc  = 0x00000000
xorOut   = 0xFFFFFFFF
crcValue = 0x00000000'''
assert str(crc) == str_rep
assert crc.digest() == b'\x00\x00\x00\x00'
assert crc.hexdigest() == '00000000'

crc.update(msg)
assert crc.crcValue == 0x84BFF58
assert crc.digest() == b'\x08\x4b\xff\x58'
assert crc.hexdigest() == '084BFF58'

x = crc.copy()
assert x is not crc
str_rep = '''poly = 0x104C11DB7
reverse = True
initCrc  = 0x00000000
xorOut   = 0xFFFFFFFF
crcValue = 0x084BFF58'''
assert str(crc) == str_rep
assert str(x) == str_rep

y = crc.new()
assert y is not crc
assert y is not x
str_rep = '''poly = 0x104C11DB7
reverse = True
initCrc  = 0x00000000
xorOut   = 0xFFFFFFFF
crcValue = 0x00000000'''
assert str(y) == str_rep

#-----------------------------------------------------------------------------
# Verify the predefined CRCs

# Verify predefined CRC functions
test(mkPredefinedCrcFun('crc-aug-ccitt'), 0xD6ED, 0x5637)
test(mkPredefinedCrcFun('x-25'), 0xE4D9, 0x0A91)
test(mkPredefinedCrcFun('crc-32'), 0xBE047A60, 0x084BFF58)

# Verify predefined CRC classes
crc1 = PredefinedCrc('crc-32')
crc1.update(msg)
assert crc1.crcValue == 0x84BFF58
crc2 = crc1.new()
assert crc1.crcValue == 0x84BFF58
assert crc2.crcValue == 0x00000000
crc2.update(msg)
assert crc1.crcValue == 0x84BFF58
assert crc2.crcValue == 0x84BFF58

for table_entry in _predefined_crc_definitions:
    # Check predefined function
    crc_func = mkPredefinedCrcFun(table_entry['name'])
    calc_value = crc_func(b"123456789")
    if calc_value != table_entry['check']:
        raise Exception("Check failed for predefined algorithm '%s'" % table_entry['name'])

    # Check predefined class
    crc1 = PredefinedCrc(table_entry['name'])
    crc1.update(b"123456789")
    if crc1.crcValue != table_entry['check']:
        raise Exception("Check failed for predefined algorithm '%s'" % table_entry['name'])

print('All tests PASS')

#-----------------------------------------------------------------------------
# Demonstrate the use of the code generator

print('Generating examples.c')
out = open('examples.c', 'w')
out.write('''// Define the required data types
typedef unsigned char      UINT8;
typedef unsigned short     UINT16;
typedef unsigned int       UINT32;
typedef unsigned long long UINT64;
''')
Crc(g8, rev=False).generateCode('crc8',out)
Crc(g8, rev=True).generateCode('crc8r',out)
Crc(g16, rev=False).generateCode('crc16',out)
Crc(g16, rev=True).generateCode('crc16r',out)
Crc(g24, rev=False).generateCode('crc24',out)
Crc(g24, rev=True).generateCode('crc24r',out)
Crc(g32, rev=False).generateCode('crc32',out)
Crc(g32, rev=True).generateCode('crc32r',out)
Crc(g64b, rev=False).generateCode('crc64',out)
Crc(g64b, rev=True).generateCode('crc64r',out)

# Check out the XOR-out feature.
Crc(g16, initCrc=0, rev=True, xorOut=~0).generateCode('crc16x',out)
Crc(g24, initCrc=0, rev=True, xorOut=~0).generateCode('crc24x',out)
Crc(g32, initCrc=0, rev=True, xorOut=~0).generateCode('crc32x',out)
Crc(g64b, initCrc=0, rev=True, xorOut=~0).generateCode('crc64x',out)

out.close()
print('Done')

