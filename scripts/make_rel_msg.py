#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import codecs
from os.path import abspath, dirname, join
import re


def my_modifier(args, active_modifier_block):
    return (args.modifier and
            active_modifier_block.lower() == args.modifier.lower())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('version')
    parser.add_argument('--modifier')
    args = parser.parse_args()
    active_version_block = None
    with codecs.open(join(abspath(dirname(__file__)), '..', 'CHANGELOG.md'),
                     encoding='utf-8') as changelog_f:
        for line in changelog_f:
            version_m = re.match(r'\# OstrichLib v([\d\.]+)', line)
            if version_m:
                print(line.strip())
                active_version_block = version_m.group(1)
                active_modifier_block = None
            elif active_version_block == args.version:
                mod_m = re.match(r'\#\# v{} (\w+)'.format(args.version), line)
                if mod_m:
                    active_modifier_block = mod_m.group(1)
                    if my_modifier(args, active_modifier_block):
                        print('## Notes for {}'.format(active_modifier_block))
                else:
                    if (active_modifier_block is None or
                            my_modifier(args, active_modifier_block)):
                        print(line.strip())


if __name__ == '__main__':
    main()
