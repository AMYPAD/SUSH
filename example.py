#!/usr/bin/env python
"""
Example of a self-updating pure Python module with no external dependencies
"""
from __future__ import print_function
from argparse import ArgumentParser
from os import path
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import json
import logging
REPO = "https://raw.githubusercontent.com/AMYPAD/SUSH/main/"
name = path.basename(__file__)
ver = "ver.json"
log = logging.getLogger(name)
__version__ = json.load(open(ver))[name]


def get_main_parser():
    parser = ArgumentParser(prog=name, version=__version__)
    parser.add_argument("-U", "--upgrade", action="store_true")
    return parser


def main(argv=None):
    parser = get_main_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    if args.upgrade:
        log.debug("fetching %s", REPO + ver)
        upstream_ver = json.load(urlopen(REPO + ver))[name]
        if upstream_ver.split('.') > __version__.split('.'):
            log.warning("overwriting self")
            log.debug("fetching %s", REPO + name)
            upstream = urlopen(REPO + name).read()
            with open(__file__, "w") as fo:
                fo.write(upstream)
        else:
            log.info("already up-to-date")


if __name__ == "__main__":
    main()
