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
        from pysol_cards.random import RandomBase
        from pysol_cards.single_deal_args_parse import SingleDealArgsParser
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

    def test_pysolfc_text__using_named_args(self):
        from pysol_cards.cards import CardRenderer
        from pysol_cards.deal_game import Game
        from pysol_cards.random_base import RandomBase
        deal_s = Game(
            game_id="freecell",
            game_num=300000000000,
            which_deals=RandomBase.DEALS_PYSOLFC,
            max_rank=13
        ).calc_layout_string(
            CardRenderer(print_ts=True)
        )
        # /usr/bin/make_pysol_freecell_board.py -F -t 300000000000 freecell
        self.assertEqual(
            deal_s,
            """4S KD 6H 2D QC 4D AH
QS 7S 5C AS KC 6S 8H
TH JC 9S 2C 3D 4H 7D
5S 4C 8D 7C JD 8C JS
QH TS AC KS TC 5H
6C 9D 9H 2H JH 3C
9C 2S 8S 3H 6D QD
KH 3S TD 5D 7H AD
""",
            "pysolfc deal #300000000000",
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

    def test_pysolfc_binary_star(self):
        from pysol_cards.cards import CardRenderer
        from pysol_cards.deal_game import Game
        from pysol_cards.random_base import RandomBase
        deal_s = Game(
            game_id="binary_star",
            game_num=240000,
            which_deals=RandomBase.DEALS_PYSOLFC,
            max_rank=13
        ).calc_layout_string(
            CardRenderer(print_ts=True)
        )
        # make_pysol_freecell_board.py -F -t 240000 binary_star
        self.assertEqual(
            deal_s,
            """Foundations: AS KH
5H 6H 2C QD 4H 4C
2S KH 5D 9D 4H 6C
KC KS 5S TS QD TH
JH QH 5D 6H 7H 7H
7D QS QC JS TH AH
AD 9D 2S 7S 6D JD
AH KD 2C 3H 3S 8H
TD 8H 7C 4S JC 7C
8S AC 4S 3C QC 9S
KC KS 9C JD AS 9C
2H 7D TC 4D 9H 8C
QS 7S 6D 3D 6C TD
4C 5H 5C 5S JS 3H
9S 5C TS 2H 4D 3S
KD AC QH 6S 3D 3C
2D 8C 6S 8D TC 9H
8D 8S JH JC AD 2D
""",
            "pysolfc binary_star deal #240000",
        )
