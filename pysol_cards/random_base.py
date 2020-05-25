#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under terms of the MIT license.

from pysol_cards.errors import SubclassResponsibility


class RandomBase(object):
    DEALS_PYSOL = 0
    DEALS_PYSOLFC = 1
    DEALS_MS = 2

    MAX_SEED = 10 ** 20
    ORIGIN_UNKNOWN = 0
    ORIGIN_RANDOM = 1
    ORIGIN_PREVIEW = 2
    ORIGIN_SELECTED = 3
    ORIGIN_NEXT_GAME = 4

    def __init__(self, seed=None):
        """docstring for __init__"""
        self.seed_as_string = None

    def shuffle(self, seq):
        for n in range(len(seq) - 1, 0, -1):
            j = self.randint(0, n)
            seq[n], seq[j] = seq[j], seq[n]
        return seq

    def randint(self, a, b):
        """ Get a random integer in the range [a, b] including both ends."""
        return a + int(self.random() * (b + 1 - a))

    def randrange(self, a, b):
        """ Get a random integer in the range [a, b) excluding b."""
        return self.randint(a, b - 1)

    def choice(self, sequence):
        """ Pick a random element of sequence """
        return sequence[self.randrange(0, len(sequence))]

    def setSeedAsStr(self, new_s):
        self.seed_as_string = new_s

    def getSeedAsStr(self):
        if self.seed_as_string:
            return self.seed_as_string
        return str(self)

    def getSeedStr(self):
        return str(self.initial_seed)

    def __str__(self):
        return self.str(self.initial_seed)

    def str(self, seed):
        return '%020d' % (seed)

    def increaseSeed(self, seed):
        if seed < self.MAX_SEED:
            return seed + 1
        return 0

    def copy(self):
        ret = self.__class__()
        ret.__dict__.update(self.__dict__)
        return ret

    def reset(self):
        raise SubclassResponsibility

    def _getRandomSeed(self):
        import time
        ret = int(time.time() * 256.0)
        return ((ret ^ (ret >> 24)) % (self.MAX_SEED + 1))

    def getstate(self):
        """getstate() for PySolFC"""
        return self.seed

    def setstate(self, new_state):
        """set to a new state"""
        self.seed = new_state
