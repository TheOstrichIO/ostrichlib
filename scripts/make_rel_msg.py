#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import codecs
from os.path import abspath, dirname, join
import re


def my_modifier(modifier, active_modifier_block):
    return (modifier and active_modifier_block.lower() == modifier.lower())


def get_filtered_changelog(version, modifier=None):
    changelog = []
    active_version_block = None
    with codecs.open(join(abspath(dirname(__file__)), '..', 'CHANGELOG.md'),
                     encoding='utf-8') as changelog_f:
        for line in changelog_f:
            version_m = re.match(r'\# OstrichLib v([\d\.]+)', line)
            if version_m:
                active_version_block = version_m.group(1)
                active_modifier_block = None
                if active_version_block == version:
                    if modifier:
                        changelog.append(
                            'OstrichLib {} {}\n'.format(version, modifier))
                    else:
                        changelog.append('OstrichLib {}\n'.format(version))
            elif active_version_block == version:
                mod_m = re.match(r'\#\# v{} (\w+)'.format(version), line)
                if mod_m:
                    active_modifier_block = mod_m.group(1)
                    if my_modifier(modifier, active_modifier_block):
                        changelog.append(
                            '## Notes for {}\n'.format(active_modifier_block))
                else:
                    if (active_modifier_block is None or
                            my_modifier(modifier, active_modifier_block)):
                        changelog.append(line)
    return ''.join(changelog).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('version')
    parser.add_argument('--modifier')
    args = parser.parse_args()
    print(get_filtered_changelog(args.version, args.modifier))


if __name__ == '__main__':
    main()
