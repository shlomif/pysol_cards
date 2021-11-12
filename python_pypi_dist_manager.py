#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the MIT license.

import sys

from pydistman import DistManager


try:
    cmd = sys.argv.pop(1)
except IndexError:
    cmd = 'build'

dist_name = "pysol_cards"

obj = DistManager(
    dist_name=dist_name,
    dist_version="0.14.1",
    project_name="pysol_cards",
    project_short_description="Deal PySol FC Cards",
    release_date="2021-11-11",
    project_year="2020",
    aur_email="shlomif@cpan.org",
    project_email="shlomif@cpan.org",
    full_name="Shlomi Fish",
    github_username="shlomif",
)
obj.run_command(cmd=cmd, args=[])
