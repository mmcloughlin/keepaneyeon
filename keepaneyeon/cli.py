import sys
import argparse

import keepaneyeon.config

def main():
    parser = argparse.ArgumentParser(
        description='Fetch URLs and record changes')
    parser.add_argument('config', action='store', type=argparse.FileType('r'),
            default=sys.stdin, help='configuration file')
    args = parser.parse_args()

    cfg = keepaneyeon.config.load(args.config)
    for target in cfg['targets']:
        target.fetch()
