#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the MIT license.

from pydistman import DistManager


class Derived(DistManager):
    """docstring for Derived"""
    pass


dist_name = "pysol_cards"

obj = Derived(
    dist_name=dist_name,
    dist_version="0.16.0",
    project_name="pysol_cards",
    project_short_description="Deal PySol FC Cards",
    release_date="2024-01-05",
    project_year="2020",
    aur_email="shlomif@cpan.org",
    project_email="shlomif@cpan.org",
    full_name="Shlomi Fish",
    github_username="shlomif",
    filter_test_reqs=True,
)
obj.cli_run()
