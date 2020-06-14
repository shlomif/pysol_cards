# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under terms of the MIT license.

"""

"""

from pysol_cards.random import RandomBase


class SingleDealArgsParser(object):
    def __init__(self, args):
        self.print_ts = False
        self.which_deals = RandomBase.DEALS_PYSOL
        self.max_rank = 13
        while args[1][0] == '-':
            a = args[1]
            args.pop(1)
            if a == "-t":
                self.print_ts = True
            elif (a == "--max-rank"):
                self.max_rank = int(args.pop(1))
            elif (a == "--pysolfc") or (a == "-F"):
                self.which_deals = RandomBase.DEALS_PYSOLFC
            elif (a == "--ms") or (a == "-M"):
                self.which_deals = RandomBase.DEALS_MS
            else:
                raise ValueError("Unknown flag " + a + "!")

        self.game_num = int(args[1])
        self.which_game = args[2] if len(args) >= 3 else "freecell"
