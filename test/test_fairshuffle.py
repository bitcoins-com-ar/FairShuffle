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

from fairshuffle import FairShuffle, FairShuffleError
from binascii import unhexlify
from pytest import raises

BLOCK_LENGTH = 32
GENESIS_BLOCK = b"\x00" * BLOCK_LENGTH

class TestErrors(object):
    def test_hash_too_short(self):
        with raises(FairShuffleError):
            FairShuffle('test').shuffle('\x00' * (BLOCK_LENGTH - 1))

    def test_hash_too_long(self):
        with raises(FairShuffleError):
            FairShuffle('test').shuffle('\x00' * (BLOCK_LENGTH + 1))

class TestEmpty(object):
    def test_empty(self):
        assert(FairShuffle(None).shuffle(GENESIS_BLOCK) == [])

class TestBasics(object):
    def test_genesis_block(self):
        assert(FairShuffle(0).shuffle(GENESIS_BLOCK) ==  [0,])
        assert(FairShuffle(1).shuffle(GENESIS_BLOCK) ==  [1,])
        assert(FairShuffle((0,)).shuffle(GENESIS_BLOCK) ==  (0,))
        assert(FairShuffle([1,]).shuffle(GENESIS_BLOCK) ==  [1,])
        assert(FairShuffle((0, 1)).shuffle(GENESIS_BLOCK) ==  (1, 0))
        assert(FairShuffle([1, 0]).shuffle(GENESIS_BLOCK) ==  [0, 1])
        assert(FairShuffle((1, 0, 1)).shuffle(GENESIS_BLOCK) ==  (1, 1, 0))
        assert(FairShuffle((0, 1, 0)).shuffle(GENESIS_BLOCK) ==  (0, 0, 1))
        
        assert(FairShuffle(0x00).shuffle(GENESIS_BLOCK) ==  [0x00,])
        assert(FairShuffle(0xFF).shuffle(GENESIS_BLOCK) ==  [0xFF,])
        assert(FairShuffle([0x01, 0x02, 0x03]).shuffle(GENESIS_BLOCK) ==  [0x03, 0x01, 0x02])
        assert(FairShuffle((0xC0, 0xFF, 0xEE)).shuffle(GENESIS_BLOCK) ==  (0xEE, 0xC0, 0xFF))
        
        assert(FairShuffle('test').shuffle(GENESIS_BLOCK) ==  ['test'])
        assert(FairShuffle(['test-list',]).shuffle(GENESIS_BLOCK) ==  ['test-list',])
        assert(FairShuffle(('test-tuple',)).shuffle(GENESIS_BLOCK) ==  ('test-tuple',))
        assert(FairShuffle(('this', 'order', 'in')).shuffle(GENESIS_BLOCK)
            == ('in', 'this', 'order'))

class TestCheckpoints(object):
    def test_checkpoints(self):
        """
        Genesis + Checkpoint blocks, as used in official client source:-
        ref: https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp
        
        These are expected results for input of tuple with 10 elements 
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        """
        CHECKPOINTS = {
                 0 : {
                'hash'             : unhexlify('0000000000000000000000000000000000000000000000000000000000000000'),  
                'expected_result' : (2, 4, 7, 9, 10, 8, 3, 6, 1, 5) },
             11111 : {
                'hash'             : unhexlify('0000000069e244f73d78e8fd29ba2fd2ed618bd6fa2ee92559f542fdb26e7c1d'),  
                'expected_result' : (5, 4, 6, 3, 10, 7, 8, 1, 9, 2) },
             33333 : {        
                'hash'             : unhexlify('000000002dd5588a74784eaa7ab0507a18ad16a236e7b1ce69f00d7ddfb5d0a6'),  
                'expected_result' : (7, 9, 5, 8, 4, 3, 6, 2, 10, 1) },
             74000 : {
                'hash'             : unhexlify('0000000000573993a3c9e41ce34471c079dcf5f52a0e824a81e7f953b8661a20'),
                'expected_result' : (10, 7, 1, 2, 9, 8, 4, 6, 3, 5) },
            105000 : {
                'hash'             : unhexlify('00000000000291ce28027faea320c8d2b054b2e0fe44a773f3eefb151d6bdc97'),
                'expected_result' : (9, 3, 4, 6, 7, 1, 10, 8, 5, 2) },
            134444 : {
                'hash'             : unhexlify('00000000000005b12ffd4cd315cd34ffd4a594f430ac814c91184a0d42d2b0fe'),
                'expected_result' : (5, 4, 3, 8, 9, 1, 6, 2, 7, 10) },
            168000 : {
                'hash'             : unhexlify('000000000000099e61ea72015e79632f216fe6cb33d7899acb35b75c8303b763'),
                'expected_result' : (9, 3, 5, 6, 1, 10, 8, 7, 2, 4) },
            193000 : {
                'hash'             : unhexlify('000000000000059f452a5f7340de6682a977387c17010ff6e6c3bd83ca8b1317'),
                'expected_result' : (7, 3, 8, 9, 5, 4, 2, 1, 10, 6) },
            210000 : {
                'hash'             : unhexlify('000000000000048b95347e83192f69cf0366076336c639f9b7228e9ba171342e'),
                'expected_result' : (4, 8, 3, 1, 7, 9, 2, 6, 5, 10) },
            216116 : {
                'hash'             : unhexlify('00000000000001b4f4b433e81ee46494af945cf96014816a4e2370f11b23df4e'),
                'expected_result' : (8, 10, 1, 7, 5, 2, 6, 4, 3, 9) },
            225430 : {
                'hash'             : unhexlify('00000000000001c108384350f74090433e7fcf79a606b8e797f065b130575932'),
                'expected_result' : (8, 4, 5, 9, 3, 7, 1, 10, 6, 2) },
            250000 : {
                'hash'             : unhexlify('000000000000003887df1f29024b06fc2200b55f8af8f35453d7be294df2d214'),
                'expected_result' : (6, 4, 9, 2, 8, 1, 10, 7, 3, 5) },
            279000 : {
                'hash'             : unhexlify('0000000000000001ae8c72a0b0c301f67e3afca10e819efa9041e458e9bd7e40'),
                'expected_result' : (7, 5, 3, 6, 1, 9, 8, 10, 2, 4) },
            295000 : {
                'hash'             : unhexlify('00000000000000004d9b4ef50f0f9d686fd69db2e03af35a100370c64632a983'),
                'expected_result' : (3, 10, 9, 1, 8, 7, 5, 4, 6, 2) },
            }

        for chk in CHECKPOINTS:
            fair = FairShuffle((1, 2, 3, 4, 5, 6, 7, 8, 9 ,10))
            assert(fair.shuffle(CHECKPOINTS[chk]['hash']) == CHECKPOINTS[chk]['expected_result'])
