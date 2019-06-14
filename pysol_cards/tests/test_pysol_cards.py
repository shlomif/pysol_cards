# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_pysol_cards
----------------------------------

Tests for `pysol_cards` module.
"""

from pysol_cards.tests import base


class TestPysol_cards(base.TestCase):

    def test_something(self):
        import pysol_cards.cards

    def test_import_deal_game(self):
        import pysol_cards.deal_game

    def test_import_random(self):
        import pysol_cards.random
        class Foo(pysol_cards.random.LCRandom31):
            def bar(self):
                return super(pysol_cards.random.LCRandom31, self).shuffle([0])
        r = Foo()
        r.setSeed(5)
        self.assertEqual(r.bar(), [0], "super()")

    def test_msdeals_large_seed(self):
        from pysol_cards.cards import CardRenderer
        from pysol_cards.deal_game import Game
        from pysol_cards.random import RandomBase
        error = False
        which_deals = RandomBase.DEALS_MS
        max_rank = 13
        print_ts = True
        try:
            Game("freecell", 2 ** 33 + 1, which_deals, max_rank).print_layout(CardRenderer(print_ts))
        except ValueError:
            error = True
        self.assertEqual(error, True, "value out of range.")
        error = False
        try:
            Game("freecell", 0, which_deals, max_rank).print_layout(CardRenderer(print_ts))
        except ValueError:
            error = True
        self.assertEqual(error, True, "value out of range.")
