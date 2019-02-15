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
