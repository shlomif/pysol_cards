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

from pysol_cards.tests import base


class TestPysolCards(base.TestCase):

    def test_something(self):
        import pysol_cards.cards  # noqa: F401

    def test_import_deal_game(self):
        import pysol_cards.deal_game  # noqa: F401

    def test_import_random(self):
        import pysol_cards.random

        class Foo(pysol_cards.random.LCRandom31):
            def bar(self):
                return super(pysol_cards.random.LCRandom31, self).shuffle([0])
        r = Foo()
        r.setSeed(5)
        self.assertEqual(r.bar(), [0], "super()")

    def test_inc_seed(self):
        import pysol_cards.random

        r = pysol_cards.random.LCRandom31(200000)
        seed = r.increaseSeed(200000)
        self.assertEqual(seed, 'ms200001', "increaseSeed()")

    def test_choice(self):
        import pysol_cards.random
        r = pysol_cards.random.LCRandom64(500)
        result = r.choice([500, 600, 700])
        self.assertTrue((result in (500, 600, 700)), "choice")

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
