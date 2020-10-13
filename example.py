#!/usr/bin/env python
"""
Example of a self-updating pure Python module with no external dependencies.
"""
# MANAGED BY AUTO-UPDATE PROCESS: imports
from __future__ import print_function
from argparse import ArgumentParser
import re
from os import path

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import json
import logging

REPO = "https://raw.githubusercontent.com/AMYPAD/SUSH/main/"
SELF = path.basename(__file__)
SELF_BASE = "example.py"
VER_FILE = "ver.json"
log = logging.getLogger(SELF)
__version__ = json.load(open(VER_FILE))[SELF]
__licence__ = "Apache-2.0"
# END OF SECTION MANAGED BY AUTO-UPDATE PROCESS: imports

# place extra imports here


# MANAGED BY AUTO-UPDATE PROCESS: main
def searcher(pattern, text, flags=re.M | re.S):
    res = re.search(
        pattern.format(msg="MANAGED BY AUTO-UPDATE PROCESS:", end="END OF SECTION"),
        text,
        flags=flags,
    )
    try:
        return res.group()
    except AttributeError:
        raise ValueError("could not find %r" % pattern)


def get_main_parser():
    parser = ArgumentParser(prog=SELF, description=__doc__)
    parser.add_argument(
        "-U", "--upgrade", action="store_true", help="download latest script"
    )
    parser.add_argument("--framework-upgrade", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    return parser


def main(argv=None):
    parser = get_main_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    if args.upgrade:
        log.debug("fetching %s", REPO + VER_FILE)
        upstream_ver = json.load(urlopen(REPO + VER_FILE))[SELF]
        if upstream_ver.split(".") > __version__.split("."):
            log.warning("overwriting self")
            log.debug("fetching %s", REPO + SELF)
            upstream = urlopen(REPO + SELF).read()
            with open(__file__, "w") as fo:
                fo.write(upstream)
        else:
            log.info("already up-to-date")
    if args.framework_upgrade:
        log.debug("fetching %s", REPO + SELF_BASE)
        upstream = urlopen(REPO + SELF_BASE).read()
        self = open(__file__).read()
        update = "".join(
            (
                searcher(r".*(?=# {msg} imports)", self),
                searcher(r"# {msg} imports.*# {end} {msg} imports\n", upstream),
                searcher(r"(?<=\# {end} {msg} imports\n).*(?=\# {msg} main)", self),
                searcher(r"# {msg} main.*# {end} {msg} main\n", upstream),
                searcher(r"(?<=\# {end} {msg} main\n).*", self),
            )
        )
        with open(__file__, "w") as fo:
            fo.write(update)


if __name__ == "__main__":
    main()
# END OF SECTION MANAGED BY AUTO-UPDATE PROCESS: main
