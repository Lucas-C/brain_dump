#!/usr/bin/python3

from __future__ import print_function
import argparse, shutil, subprocess, sys

from brain_dump.graphviz import create_solarized_mindmap_img


def main(argv=None):
    print('Using command:', subprocess.check_output([shutil.which('twopi'), '-V'], stderr=subprocess.STDOUT).decode('utf8'), end='', file=sys.stderr)
    args = parse_args(argv)
    create_solarized_mindmap_img(**args.__dict__)

def parse_args(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, fromfile_prefix_chars='@')
    parser.add_argument('--layout', default='twopi', choices=('dot', 'fdp', 'neato', 'sfdp', 'twopi'), help=' ')
    parser.add_argument('--font', default='arial')
    parser.add_argument('--gen-dot-file', action='store_true')
    parser.add_argument('--hide-branches-from-id', type=int)
    parser.add_argument('--root-label')
    parser.add_argument('input_filepath')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main()
