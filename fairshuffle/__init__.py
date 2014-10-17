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

"""

__version__ = '0.1'
EXPECTED_HASH_LENGTH = 256 / 8 # 256 bit blockchain hash

import binascii, sys
PY3 = sys.version_info[0] >= 3

# Use old random from Python2 for Python3 to guarantee same PRNG routines
if PY3:
    import random2 as random
else:
    import random

class FairShuffleError(Exception):
    pass

class FairShuffle(object):
    def __init__(self, items=None):
        """
        Create a FairShuffle object.
		
        Arguments: items - a list, tuple, string, integer or None
        """
        if items is None:
            self._items = []
        elif isinstance(items, list) or isinstance(items, tuple):
            self._items = items
        elif isinstance(items, int) or isinstance(items, str):
            self._items = [items,]
        else:
            raise FairShuffleError(
                'argument of None, string, integer, list or tuple is required')
           
    # Shuffles and returns list, based on hash of bc blockchain
    
    def shuffle(self, bcHashStr):
        """
        Shuffle the elements in the listCreate a FairShuffle object.
		
        Arguments: bcHashStr - a 32 byte hash
        Returns:   a list or tuple of a fair shuffle based on hash
        """
        if not len(bcHashStr) == EXPECTED_HASH_LENGTH:
            raise FairShuffleError('invalid blockchain hash value - must be %d bytes'
                % EXPECTED_HASH_LENGTH)
        
        # Quickly return waste of time shuffles
        if len(self._items) == 0:
            return([])
        elif len(self._items) == 1:
            if isinstance(self._items, tuple):
                return (self._items[0],)
            else:
                return [self._items[0],]

        # A 32-bit unsigned integer is enough, and this was the only
        # way to get Python2/Python3 PRNGs compatible with each other.
        crc = binascii.crc32(bcHashStr) & 0xffffffff

        random.seed(crc)        
        lst = list(self._items)
        random.shuffle(lst)

        if isinstance(self._items, tuple):
            return tuple(lst)
        else:
            return lst
