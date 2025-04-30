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

Tests for `pysol_cards.cwrap` module.
"""

from unittest import TestCase


class TestPysolCards(TestCase):
    def test_pysolfc_black_hole(self):
        from pysol_cards.cwrap import create_gen
        DEALS_PYSOLFC = 1
        gen = create_gen("black_hole", DEALS_PYSOLFC)
        deal_idx = 240000
        deal_s = gen(deal_idx)
        # make_pysol_freecell_board.py -F -t 240000 black_hole
        self.assertEqual(
            deal_s,
            """Foundations: AS
3S 8H JH
7H 9C 5C
6H 5H 8S
5S 2S 3C
8D 3H 4H
5D TD AH
KC 3D 7S
4S QC QH
TC AC 2C
6C 9H 4D
TH JD KS
JC 7C 4C
QS AD 2H
9D 6D 8C
7D KD JS
2D 9S TS
6S QD KH
""",
            "pysolfc black_hole deal #240000",
        )
