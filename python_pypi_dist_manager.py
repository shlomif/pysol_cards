#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the MIT license.


import os
import os.path
import shutil

from pydistman import DistManager


class Derived(DistManager):
    """docstring for Derived"""
    def _fmt_unlink(self, fn_proto):
        """rmtree the formatted fn_proto if it exists."""
        fn = self._myformat(fn_proto)
        if os.path.exists(fn):
            os.unlink(fn)

    def _build_only_command_custom_steps(self):
        # Fix/workaround for https://github.com/shlomif/pysol_cards/issues/9
        #
        # This issue may probably affect other pydistman-based distributions:
        #
        # https://github.com/shlomif/pydistman
        self._fmt_unlink("{dest_dir}/release")
        self._fmt_unlink("{dest_dir}/pysol_cards/__main__.py")
        self._fmt_unlink("{dest_dir}/pysol_cards/template.py")
        self._fmt_unlink("{dest_dir}/tests/__init__.py")
        self._fmt_unlink("{dest_dir}/tests/test_sanity.py")


dist_name = "pysol_cards"

obj = Derived(
    dist_name=dist_name,
    dist_version="0.18.0",
    project_name="pysol_cards",
    project_short_description="Deal PySol FC Cards",
    release_date="2024-09-15",
    project_year="2020",
    aur_email="shlomif@cpan.org",
    project_email="shlomif@cpan.org",
    full_name="Shlomi Fish",
    github_username="shlomif",
    filter_test_reqs=True,
)
obj.cli_run()
