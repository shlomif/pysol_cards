# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under terms of the MIT license.

"""

"""

from pysol_cards.random import RandomBase
from pysol_cards.random import match_ms_deal_prefix


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

        game_num_s = args[1]
        msgame = match_ms_deal_prefix(game_num_s)
        if msgame is not None:
            if self.which_deals == RandomBase.DEALS_MS or \
                    self.which_deals == RandomBase.DEALS_PYSOL:
                self.which_deals = RandomBase.DEALS_MS
                self.game_num = msgame
            else:
                raise ValueError("ms deals mismatch")
        else:
            self.game_num = int(game_num_s)
        self.which_game = args[2] if len(args) >= 3 else "freecell"
