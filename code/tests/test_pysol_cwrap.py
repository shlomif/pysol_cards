# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the MIT / Expat license:
#
# https://en.wikipedia.org/wiki/MIT_License

"""

code/tests/test_pysol_cwrap.py
------------------------------

Tests for `pysol_cards.cwrap` module.

"""

from unittest import TestCase


class TestPysolCards(TestCase):
    def test_cwrap_pysolfc_black_hole(self):
        from pysol_cards.cwrap import create_gen
        DEALS_PYSOLFC = 1
        generator = create_gen("black_hole", DEALS_PYSOLFC)
        deal_idx = 240000
        deal_s = generator(deal_idx)
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
        deal_idx = 3700037
        deal_s = generator(deal_idx)
        # make_pysol_freecell_board.py -F -t 240000 black_hole
        self.assertEqual(
            deal_s,
            """Foundations: AS
2D 5C 4C
AD 6C 8C
7C TD JC
4H JH 5D
KD 3H KS
AH 6S 7S
4D 6D QH
9S KH 2H
3D 7D 3S
5S 4S 7H
JD AC TH
2C TS QC
TC 6H QS
9C 9H 3C
9D 8H 8S
QD KC 8D
JS 5H 2S
""",
            "pysolfc black_hole deal #3700037",
        )

    def test_cwrap_ms_freecell(self):
        from pysol_cards.cwrap import create_gen
        variant = "freecell"
        DEALS_MS = 0
        generator = create_gen(variant, DEALS_MS)
        deal_idx = 240002
        deal_s = generator(deal_idx)
        # /usr/bin/pi-make-microsoft-freecell-board -t 240002
        wanted_deal_s = """4C AH 8D TH QS 4S JC
AC 8S 3D 5S 4H 9H KS
3S 8C QC 7D 6C 9S KH
7S KC 9D 4D 2S TC AS
9C 5D QD 6S 2H AD
6D 5H 2D JD QH TD
JS KD 5C 7C 6H 8H
3C 3H JH TS 7H 2C
"""

        self.assertEqual(
            deal_s,
            wanted_deal_s,
            "pysolfc freecell ms deal #240002",
        )
