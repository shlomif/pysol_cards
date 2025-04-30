#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2025 Shlomi Fish < https://www.shlomifish.org/ >
#
# Licensed under the terms of the MIT license.

"""

        from pysol_cards.cwrap import create_gen
        variant = "freecell"
        DEALS_MS = 0
        gen = create_gen(variant, DEALS_MS)
        deal_idx = 240002
        deal_s = gen(deal_idx)

"""

from pysol_cards.cards import CardRenderer
from pysol_cards.deal_game import Game
from pysol_cards.random import RandomBase


_r = CardRenderer(True)


def create_gen(game_variant, ms):
    which_deals = (
        RandomBase.DEALS_MS if (ms == 0) else RandomBase.DEALS_PYSOLFC
    )
    game = Game(game_variant, 1, which_deals, 13)

    def _ret(deal_idx):
        return game.calc_deal_string(deal_idx, _r)
    return _ret
