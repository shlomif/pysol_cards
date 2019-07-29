#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under terms of the MIT license.


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

    def __init__(self):
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
