#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import os
import subprocess
import tempfile

import ostrich

from make_rel_msg import get_filtered_changelog


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', default=ostrich.__version__)
    parser.add_argument('--rc', action='store_true', help='Release a RC')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.rc:
        assert 'rc' in args.version
        version, rc = args.version.split('rc')
        modifier = 'RC{}'.format(rc)
        tag = 'v{}-rc{}'.format(version, rc)
    else:
        assert 'rc' not in args.version
        version = args.version
        modifier = None
        tag = 'v{}'.format(version)
    release_msg = get_filtered_changelog(version, modifier)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                     delete=False) as rel_msg_f:
        rel_msg_path = rel_msg_f.name
        rel_msg_f.write(release_msg)
    hub_cmd = ['hub', 'release', 'create']
    if args.rc:
        hub_cmd.append('-p')
    hub_cmd.extend(['-f', rel_msg_path, tag])
    try:
        if args.dry_run:
            print(hub_cmd)
        else:
            subprocess.run(hub_cmd)
    finally:
        os.remove(rel_msg_path)


if __name__ == '__main__':
    main()
