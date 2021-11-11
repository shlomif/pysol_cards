===============================
pysol_cards
===============================

Deal PySol FC Cards

The pysol-cards python modules allow the python developer to generate the
initial deals of some PySol FC games. It also supports PySol legacy deals
and Microsoft FreeCell / Freecell Pro deals.

* Free software: Expat license
* Documentation: pydoc
* Source: https://github.com/shlomif/pysol_cards
* Bugs: https://github.com/shlomif/pysol_cards/issues

--------

Example:
--------

::

        from pysol_cards.cards import CardRenderer
        from pysol_cards.deal_game import Game
        from pysol_cards.random_base import RandomBase
        ms24_str = Game(
            game_id="freecell",
            game_num=24,
            which_deals=RandomBase.DEALS_MS,
            max_rank=13
        ).calc_layout_string(
            CardRenderer(print_ts=True)
        )
        print(ms24_str, end='')

