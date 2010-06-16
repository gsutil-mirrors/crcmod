
============
Introduction
============

The software in this package is a Python module for generating objects that
compute the Cyclic Redundancy Check (CRC).  It includes a (optional) C
extension for fast calculation, as well as a pure Python implementation.

There is no attempt in this package to explain how the CRC works.  There are a
number of resources on the web that give a good explanation of the algorithms.
Just do a Google search for "crc calculation" and browse till you find what you
need.  Another resource can be found in chapter 20 of the book "Numerical
Recipes in C" by Press et. al.

This package allows the use of any 8, 16, 24, 32, or 64 bit CRC.  You can
generate a Python function for the selected polynomial or an instance of the
:class:`crcmod.Crc` class which provides the same interface as the
:mod:`hashlib`, :mod:`md5` and :mod:`sha` modules from the Python standard
library.  A :class:`crcmod.Crc` class instance can also generate C/C++ source
code that can be used in another application.

----------
Guidelines
----------

Documentation is available here as well as from the doc strings.

It is up to you to decide what polynomials to use in your application.  Some
common CRC algorithms are predefined in :mod:`crcmod.predefined`.  If someone
has not specified the polynomials to use, you will need to do some research to
find one suitable for your application.  Examples are available in the unit
test script :file:`test_crcmod.py` and the timing script
:file:`timing_test.py`.

If you need to generate code for another language, I suggest you subclass the
:class:`crcmod.Crc` class and replace the method
:meth:`crcmod.Crc.generateCode`.  Use :meth:`crcmod.Crc.generateCode` as a
model for the new version.

------------
Dependencies
------------

Python Version
^^^^^^^^^^^^^^

The module has separate code to support the 2.x and 3.x Python series.

For the 2.x versions of Python, these versions have been tested:

* 2.4
* 2.5
* 2.6
* 2.7

It may still work on earlier versions of Python 2.x, but these have not been
recently tested.

For the 3.x versions of Python, these versions have been tested:

* 3.1

Building C extension
^^^^^^^^^^^^^^^^^^^^

To build the C extension, the appropriate compiler tools for your platform must
be installed. Refer to the Python documentation for building C extensions for
details.

------------
Installation
------------

The :mod:`crcmod` package is installed using :mod:`distutils`.  If you have the
tools installed to build a Python extension module, run the following command::

   python setup.py install

If you don't have the tools to build an extension module, you will need to
install the pure Python version using the following command::

   python setup_py.py install

For Python 3.x, the install process is the same but you need to use the 3.x
interpreter.

------------
Unit Testing
------------

The :mod:`crcmod` module has a sub-module :mod:`crcmod.test`, which contains
unit tests for both :mod:`crcmod` and :mod:`crcmod.predefined`.

When you first install :mod:`crcmod`, you should run the unit tests to make
sure everything is installed properly.  The unit tests perform a number of
tests including a comparison to the direct method which uses a class
implementing polynomials over the integers mod 2.

To run the unit tests on Python >=2.5::

    python -m crcmod.test

Alternatively, in the :file:`test` directory run::

    python test_crcmod.py

------
Timing
------

A few timing measurements were taken using the :mod:`timeit` module in the
Python standard library.  The Python implementation is compared to the
extension module, the :mod:`md5` module in the standard library, and the
:func:`binascii.crc32` function from the :mod:`binascii` module.  These
measurements were taken on my development system which is a 3GHz Pentium IV
with hyper threading running the Debian Sarge distribution of Linux with the
2.6.6 version of the kernel.  The Python version was 2.3.3.

The following result was obtained by running the :file:`timing_test.py` script
twice. Once with the Python version and once with the extension module.

======================  ============  ============  ==========================
Module                  min (µs)      max (µs)      Notes
======================  ============  ============  ==========================
:mod:`crcmod`           14981.4       15035.8       Pure Python implementation
:mod:`crcmod`           64.2          64.4          C extension module
:mod:`md5`              59.0          59.3        
:func:`binascii.crc32`  87.2          87.4        
======================  ============  ============  ==========================

* Timing in microseconds per iteration
* min and max of 10 repetitions

It is interesting that on this system, the :mod:`md5` module is slightly faster
than a 32-bit CRC even though the message digest is 128-bits and is
cryptographically more secure.  This is surprising since the MD5 code looks a
lot more complex. I tried unrolling the inner loop and using the function
interface instead of the class interface.  These changes only got the result
down to where the MD5 and CRC took about the same amount of time.

.. note::
    :func:`binascii.crc32` is slower than :mod:`crcmod` because it includes a
    mask operation to get the low order byte of a 32-bit word.  A cast is used
    in the CRC module to accomplish the same thing.

-------
License
-------

The :mod:`crcmod` module is released under the MIT license:

   Copyright (c) 2010  Raymond L. Buvel

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.


----------
References
----------

.. seealso::

   :func:`binascii.crc32` function from the :mod:`binascii` module
      CRC-32 implementation
   
   :func:`zlib.crc32` function from the :mod:`zlib` module
      CRC-32 implementation

   Module :mod:`hashlib`
      Secure hash and message digest algorithms.

   Module :mod:`md5`
      RSA's MD5 message digest algorithm.

   Module :mod:`sha`
      NIST's secure hash algorithm, SHA.

   Module :mod:`hmac`
      Keyed-hashing for message authentication.
