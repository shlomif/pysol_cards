#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2025 Shlomi Fish < https://www.shlomifish.org/ >
#
# Licensed under the terms of the MIT license.

"""
This is a module that implements a command line interface ( CLI )
for generating ranges of deals, which is used by:

https://github.com/shlomif/fc-solve/blob/master/fc-solve/source/board_gen/gen-multiple-pysol-layouts

The interface has not yet stabilized.

"""

import argparse
import os
import sys
from os.path import basename, join
from pathlib import Path

from pysol_cards.cards import CardRenderer
from pysol_cards.deal_game import Game
from pysol_cards.random import RandomBase


class DealsRange:
    def __init__(self, idxs):
        assert idxs.pop(0) == 'seq'
        self.start = int(idxs.pop(0))
        self.end = int(idxs.pop(0))
        assert self.start >= 1
        assert self.end >= self.start

    def run(self):
        return range(self.start, self.end + 1)


class GenMultiParseCmdLine:
    def __init__(self, argv):
        cliargs = argv[1:]
        if cliargs == ["--mode", "shlomif"] or cliargs == ["--mode=shlomif"]:
            self._backend = ShlomifDwimGenDeals()
            return
        parser = argparse.ArgumentParser(
            prog='PROG',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--concat', action='store_true',
                            help='concatenate the deals into one large file')
        parser.add_argument('--dir', type=str, required=True,
                            help='output dir')
        parser.add_argument('--force', action='store_true',
                            help='override deal files in existing directory')
        parser.add_argument('--game', type=str, default='freecell',
                            help='The Solitaire variant')
        parser.add_argument(
            '--mkdir', action='store_true',
            help='Make the target directory if it does not exist')
        parser.add_argument('--ms', action='store_true',
                            help='MS/FC-Pro Deals')
        parser.add_argument('--prefix', type=str, required=True,
                            help='filename prefix')
        parser.add_argument('--suffix', type=str, required=True,
                            help='filename suffix')
        parser.add_argument('idxs', nargs='+', default=[],
                            help='indexes')
        args = parser.parse_args(argv[1:])
        self._backend = GenMulti(
            concat=args.concat,
            dir_=args.dir,
            force=args.force,
            game_variant=args.game,
            idxs=args.idxs,
            mkdir_=args.mkdir,
            ms=args.ms,
            prefix=args.prefix,
            suffix=args.suffix,
        )

    def run(self):
        return self._backend.run()


class GenMulti:
    def __init__(self, concat, dir_, force, game_variant, idxs,
                 mkdir_, ms, prefix, suffix):
        self.concat = concat
        self.dir_ = dir_
        self.force = force
        self.game_variant = game_variant
        self.idxs = idxs
        self.mkdir_ = mkdir_
        # Sanitize, see:
        # https://stackoverflow.com/questions/6803505
        self.prefix = basename(prefix)
        self.suffix = basename(suffix)
        self.which_deals = (RandomBase.DEALS_MS if ms
                            else RandomBase.DEALS_PYSOLFC)

        self.rend = CardRenderer(True)
        self.game = Game(self.game_variant, 1, self.which_deals, 13)

    def _out_deal(self, deal):
        with open(join(
            self.dir_, self.prefix + str(deal) + self.suffix
        ), 'wt') as f:
            f.write(self.game.calc_deal_string(deal, self.rend))

    def run(self):
        if self.concat:
            idxs = self.idxs
            r = DealsRange(idxs=idxs)
            assert len(idxs) == 0
            with open(self.dir_, 'wt') as f:
                width = None
                for deal in r.run():
                    s = self.game.calc_deal_string(deal, self.rend)
                    w = len(s)
                    if width is None:
                        width = w
                    assert w == width
                    f.write(s)
            metadata_fn = self.dir_ + ".metadata.json"

            def i2s(i):
                assert isinstance(i, int)
                return "{}".format(i)
            which_deals = (
                "ms" if (self.which_deals == RandomBase.DEALS_MS)
                else "pysolfc"
            )
            metadata = {
                "game": self.game_variant,
                "seeds": [{
                    "end": i2s(r.end),
                    "start": i2s(r.start),
                    "type": "seq",
                }],
                "width": i2s(width),
                "which_deals": which_deals,
            }
            import json
            with open(metadata_fn, 'wt') as f:
                json.dump(metadata, f, sort_keys=True)

            return
        if self.mkdir_:
            dir_ = Path(self.dir_)
            if dir_.is_dir():
                if not self.force:
                    return
            os.makedirs(self.dir_, exist_ok=True)
        idxs = self.idxs
        while len(idxs):
            i = idxs[0]
            if i == 'seq':
                r = DealsRange(idxs=idxs)
                for deal in r.run():
                    self._out_deal(deal)
            elif i == 'slurp':
                idxs.pop(0)
                slurpfn = idxs.pop(0)
                with open(slurpfn, 'rt') as fh:
                    for line in fh:
                        self._out_deal(int(line))
            else:
                idxs.pop(0)
                self._out_deal(int(i))
        return 0


class ShlomifDwimGenDeals:
    def __init__(self):
        return

    def run(self):
        from pathlib import Path
        parent_dir = Path.home() / "Arcs" / "temp" / "solitaire" / \
            "deals" / "ms"
        os.makedirs(parent_dir, exist_ok=True)
        concat = True
        for game_variant in ["all_in_a_row", "black_hole", "freecell", "golf"]:
            dir_obj = parent_dir / game_variant
            dir_ = str(dir_obj)
            generator = GenMulti(
                concat=concat,
                dir_=dir_,
                force=False,
                game_variant=game_variant,
                idxs=["seq", "1", "32000",],
                mkdir_=True,
                ms=True,
                prefix="ms",
                suffix=".board",
            )
            generator.run()


def _cli_main():
    sys.exit(GenMultiParseCmdLine(argv=sys.argv).run())


if __name__ == "__main__":
    _cli_main()
