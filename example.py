#!python
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
import logging
REPO = "https://raw.githubusercontent.com/AMYPAD/SUSH/main/"
name = path.basename(__file__)
log = logging.getLogger(name)


def get_main_parser():
    parser = ArgumentParser(prog=name)
    parser.add_argument("-U", "--upgrade", action="store_true")
    return parser


def main(argv=None):
    parser = get_main_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    if args.upgrade:
        upstream = REPO + name
        log.info("fetching %s", upstream)
        print(upstream)
        with urlopen(upstream) as fd:
            script = fd.read()
        log.warning("overwriting self")
        with open(__file__, "w") as fo:
            fo.write(script)


if __name__ == "__main__":
    main()
