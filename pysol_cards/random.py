#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under terms of the Expat license.


from pysol_cards.cards import ms_rearrange
from pysol_cards.random_base import RandomBase

import random2


class PysolRandom(RandomBase):
    def setSeed(self, seed):
        seed = self._convertSeed(seed)
        if not 0 <= seed <= self.MAX_SEED:
            raise ValueError("seed is out of range")
        self.seed = seed
        return seed

    def _convertSeed(self, seed):
        return int(seed)

# /***********************************************************************
# // Linear Congruential random generator
# //
# // Knuth, Donald.E., "The Art of Computer Programming,", Vol 2,
# // Seminumerical Algorithms, Third Edition, Addison-Wesley, 1998,
# // p. 106 (line 26) & p. 108
# ************************************************************************/


class LCRandom64(PysolRandom):
    MAX_SEED = 0xffffffffffffffff  # 64 bits

    def random(self):
        self.seed = (self.seed * 6364136223846793005 + 1) & self.MAX_SEED
        return ((self.seed >> 21) & 0x7fffffff) / 2147483648.0


class LCRandom31(RandomBase):
    MAX_SEED = ((1 << (31 + 2)) - 1)         # 33 bits

    def setSeed(self, seed):
        if not 1 <= seed <= self.MAX_SEED:
            raise ValueError("seed is out of range")
        self.seed = seed
        self.seedx = seed if (seed < 0x100000000) else (seed - 0x100000000)

    def random(self):
        if (self.seed < 0x100000000):
            ret = self._rand()
            return (ret if (self.seed < 0x80000000) else (ret | 0x8000))
        else:
            return self._randp() + 1

    def _randp(self):
        self.seedx = ((self.seedx) * 214013 + 2531011) & self.MAX_SEED
        return (self.seedx >> 16) & 0xffff

    def _rand(self):
        self.seedx = ((self.seedx) * 214013 + 2531011) & self.MAX_SEED
        return (self.seedx >> 16) & 0x7fff

    def randint(self, a, b):
        return a + self.random() % (b + 1 - a)


# * Mersenne Twister random number generator
class MTRandom(RandomBase, random2.Random):
    MAX_SEED = 100000000000000000000  # 20 digits

    def setSeed(self, seed):
        random2.Random.__init__(self, seed)
        self.initial_state = self.getstate()


def shuffle(cards, game_num, which_deals):
    ms = ((game_num <= 32000) or (which_deals == RandomBase.DEALS_MS))
    r = LCRandom31() if ms else MTRandom() if which_deals == \
        RandomBase.DEALS_PYSOLFC else LCRandom64()
    r.setSeed(game_num)
    return r.shuffle(ms_rearrange(cards) if ms else cards)
