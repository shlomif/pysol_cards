#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the MIT license.

import re
import sys

from pydistman import DistManager


class Derived(DistManager):
    """docstring for Derived"""

    def _build_only_command_custom_steps(self):
        req_bn = "requirements.txt"
        req_fn = "{src_dir}/" + req_bn
        with open(self._myformat("{dest_dir}/tox.ini"), "wt") as ofh:
            ofh.write(
                "[tox]\nenvlist = py39\n\n" +  ## noqa
                "[testenv]\ndeps =" + "".join(
                    ["\n\t" + x for x in
                     sorted(
                         list(self._testreqs.keys()) +  ## noqa
                         self._fmt_slurp(req_fn).split("\n"))]
                ) + "\n" + ## noqa
                "\ncommands = pytest\n")
        return

    def _reqs_mutate(self, fn_proto):
        fn = self._myformat(fn_proto)
        txt = self._slurp(fn)
        d = {}
        testreqs = {}
        for line in txt.split("\n"):
            if 0 == len(line):
                continue
            m = re.match("\\A([A-Za-z0-9_\\-]+)>=([0-9\\.]+)\\Z", line)
            if m:
                req = m.group(1)
                ver = m.group(2)
            else:
                req = line
                ver = '0'
            if req in ['coverage', 'pytest', 'pytest-cov', 'requests',
                       'twine', ]:
                testreqs[req] = '0'
                continue
            if ver == '0':
                if req not in d:
                    d[req] = '0'
            else:
                if req not in d or d[req] == '0':
                    d[req] = ver
                else:
                    raise BaseException(
                        "mismatch reqs: {} {} {}".format(req, ver, d[req]))
        self._testreqs = testreqs
        self._reqs = list(sorted([
            x + ('' if v == '0' else '>=' + v) for x, v in d.items()]))
        txt = "".join([x + "\n" for x in self._reqs])
        with open(fn, "wt") as ofh:
            ofh.write(txt)


try:
    cmd = sys.argv.pop(1)
except IndexError:
    cmd = 'build'

dist_name = "pysol_cards"

obj = Derived(
    dist_name=dist_name,
    dist_version="0.14.2",
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
