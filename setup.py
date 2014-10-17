#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

This file is part of FairShuffle
Copyright © 2014 James Martin

This library is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FairShuffle.  If not, see <http://www.gnu.org/licenses/>.

FairShuffle - Fairly shuffle a list of elements, using unpredictable
but fair and verifiable values from the Bitcoin blockchain.
========================

This program utilizes the unpredictability of the Bitcoin blockchain
hash to fairly sort a list of items into a easily verified
pseudo-random order.

This guarantees every time the latest Bitcoin blockchain block is
generated, the list is ordered into a new unpredictable order.

Useful for lists of websites, people, list of donators etc... without
giving them unfair advantage for by being on top of the list.
Any interested indenpendant party can verify that the list was ordered
fairly by inspecting which blockchain generated the list.

As Bitcoin blockchain is generated every ~10 minutes, list can be
shuffled once every ~10 minutes, which is useful for caching and not
having to process the list every page view.
"""

from __future__ import print_function

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import fairshuffle

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', )

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

"""
Python 3 users require "random2" lib for compatibility as
internal random module behaves differently between Py2 / Py3 and
produces different seeding/results.
"""
if sys.version_info[0] >= 3:
	install_req = ['random2']
else:
	install_req = []

setup(
    name='fairshuffle',
    version=fairshuffle.__version__,
    url='https://github.com/bitcoins-com-ar/FairShuffle',
    license='GNU GPL v3',
    author='James Martin',
    tests_require=['pytest'],
    install_requires=install_req,
    cmdclass={'test': PyTest},
    author_email='jimpub@gmail.com',
    description='Fairly shuffle a list using Bitcoin blockchain',
    long_description=long_description,
    packages=['fairshuffle'],
    include_package_data=True,
    platforms='any',
    test_suite='fairshuffle.test.test_fairshuffle',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
