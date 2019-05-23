#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under terms of the Expat license.

"""

"""


class Card(object):
    ACE = 1
    KING = 13

    def __init__(self, id, rank, suit):
        self.id, self.rank, self.suit = id, rank, suit
        self.empty, self.flipped = False, False

    def suit_s(self):
        return 'CSHD'[self.suit]

    def is_ace(self):
        return self.rank == self.ACE

    def is_king(self):
        return self.rank == self.KING

    def flip(self, flipped=True):
        ret = Card(self.id, self.rank, self.suit)
        ret.flipped = flipped
        return ret


class CardRenderer(object):
    """docstring for CardRenderer"""
    def __init__(self, print_ts):
        self.print_ts = print_ts

    def to_s(self, card):
        if card.empty:
            return '-'
        ret = self.rank_s(card) + card.suit_s()
        if card.flipped:
            ret = '<' + ret + '>'
        return ret

    def found_s(self, card):
        return card.suit_s() + '-' + self.rank_s(card)

    def rank_s(self, card):
        ret = "0A23456789TJQK"[card.rank]
        if ((not self.print_ts) and ret == 'T'):
            ret = '10'
        return ret

    def render_l(self, lst):
        return [self.to_s(x) for x in lst]

    def l_concat(self, lst):
        return ' '.join(self.render_l(lst))


def createCards(num_decks, max_rank=13):
    ret = []
    for _ in range(num_decks):
        id = 0
        for s in range(4):
            for r in range(max_rank):
                ret.append(Card(id, r + 1, s))
                id += 1
    return ret


def ms_rearrange(cards):
    if len(cards) != 52:
        return cards
    c = []
    for i in range(13):
        for j in (0, 39, 26, 13):
            c.append(cards[i + j])
    return c
