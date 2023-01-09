# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the MIT / Expat license:
#
# https://en.wikipedia.org/wiki/MIT_License

"""
test_pysol_cards
----------------------------------

Tests for `pysol_cards` module.
"""

from unittest import TestCase

import pysol_cards.random


class TestPysolCards(TestCase):

    def test_something(self):
        import pysol_cards.cards  # noqa: F401

    def test_import_deal_game(self):
        import pysol_cards.deal_game  # noqa: F401

    def test_import_random(self):
        class Foo(pysol_cards.random.LCRandom31):
            def bar(self):
                return super(pysol_cards.random.LCRandom31, self).shuffle([0])
        r = Foo()
        r.setSeed(5)
        self.assertEqual(r.bar(), [0], "super()")

    def test_inc_seed(self):
        r = pysol_cards.random.LCRandom31(200000)
        seed = r.increaseSeed(200000)
        self.assertEqual(seed, 'ms200001', "increaseSeed()")

    def test_mtrandom_reset(self):
        r = pysol_cards.random.MTRandom(10000000)
        bef0 = r.randint(0, 100)
        bef1 = r.randint(0, 100)
        r.reset()
        aft0 = r.randint(0, 100)
        aft1 = r.randint(0, 100)
        self.assertEqual([aft0, aft1], [bef0, bef1], "MTRandom.reset()")

    def test_choice(self):
        r = pysol_cards.random.LCRandom64(500)
        result = r.choice([500, 600, 700])
        self.assertTrue((result in (500, 600, 700)), "choice")

    def test_ms_single_deal(self):
        from pysol_cards.single_deal_args_parse import SingleDealArgsParser
        from pysol_cards.random import RandomBase
        obj = SingleDealArgsParser(["dealer.py", "ms2000000", ])
        self.assertEqual(obj.which_deals, RandomBase.DEALS_MS)
        self.assertEqual(obj.game_num, 2000000)

    def test_ms_seed_prefix(self):
        from pysol_cards.random import match_ms_deal_prefix
        self.assertEqual(match_ms_deal_prefix('123'), None, "no prefix")
        self.assertEqual(match_ms_deal_prefix('ms200400'), 200400, "ms prefix")

    def test_msdeals_large_seed(self):
        from pysol_cards.cards import CardRenderer
        from pysol_cards.deal_game import Game
        from pysol_cards.random import RandomBase
        error = False
        which_deals = RandomBase.DEALS_MS
        max_rank = 13
        print_ts = True
        try:
            Game("freecell", 2 ** 33 + 1, which_deals, max_rank).print_layout(
                CardRenderer(print_ts))
        except ValueError:
            error = True
        self.assertEqual(error, True, "value out of range.")
        error = False
        try:
            Game("freecell", 0, which_deals, max_rank).print_layout(
                CardRenderer(print_ts))
        except ValueError:
            error = True
        self.assertEqual(error, True, "value out of range.")

    def test_ms24_text(self):
        from pysol_cards.cards import CardRenderer
        from pysol_cards.deal_game import Game
        from pysol_cards.random_base import RandomBase
        ms24s = Game(
            "freecell", 24,
            RandomBase.DEALS_MS,
            max_rank=13
        ).calc_layout_string(CardRenderer(True))
        self.assertEqual(
            ms24s,
            """4C 2C 9C 8C QS 4S 2H
5H QH 3C AC 3H 4H QD
QC 9S 6H 9H 3S KS 3D
5D 2S JC 5C JH 6D AS
2D KD TH TC TD 8D
7H JS KH TS KC 7C
AH 5S 6S AD 8H JD
7S 6C 7D 4D 8S 9D
""",
            "MS deal #24",
        )

    def test_ms24_text__using_named_args(self):
        from pysol_cards.cards import CardRenderer
        from pysol_cards.deal_game import Game
        from pysol_cards.random_base import RandomBase
        ms24s = Game(
            game_id="freecell",
            game_num=24,
            which_deals=RandomBase.DEALS_MS,
            max_rank=13
        ).calc_layout_string(
            CardRenderer(print_ts=True)
        )
        self.assertEqual(
            ms24s,
            """4C 2C 9C 8C QS 4S 2H
5H QH 3C AC 3H 4H QD
QC 9S 6H 9H 3S KS 3D
5D 2S JC 5C JH 6D AS
2D KD TH TC TD 8D
7H JS KH TS KC 7C
AH 5S 6S AD 8H JD
7S 6C 7D 4D 8S 9D
""",
            "MS deal #24",
        )

    def test_set_get_state(self):
        for class_, seed in [
                (pysol_cards.random.LCRandom31, 240),
                (pysol_cards.random.LCRandom31, 6 + (1 << 32)),
                (pysol_cards.random.LCRandom64, 240),
                (pysol_cards.random.LCRandom64, 20000000000),
                (pysol_cards.random.MTRandom, 10000000),
        ]:
            r = class_(seed)
            r.randint(0, 100)
            state = r.getstate()
            bef0 = r.randint(0, 100)
            bef1 = r.randint(0, 100)
            r.setstate(state)
            aft0 = r.randint(0, 100)
            aft1 = r.randint(0, 100)
            self.assertEqual([aft0, aft1], [bef0, bef1], "MTRandom.setState()")
