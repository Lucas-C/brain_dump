#!/usr/bin/python3

import argparse

from braindump.parsers.indented_text_graph import parse as parse_text_graph
from braindump.wisemapping_xml import recursively_print_map


PALETTES = {
    'dark-solarized': ( # from http://ethanschoonover.com/solarized
        '#b58900', # yellow
        '#cb4b16', # orange
        '#6c71c4', # violet
        '#dc323f', # red
        '#268bd2', # blue
        '#d33682', # magenta
        '#2aa198', # cyan
        '#859900', # green
        '#939393', # grey
    )
}

def main(argv=None):
    args = parse_args(argv=None)
    args.palette = None if args.palette == 'none' else PALETTES[args.palette]
    with open(args.input_filepath, encoding='utf8') as text_file:
        graph = parse_text_graph(text_file.read())
    recursively_print_map(graph, args)

def parse_args(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, fromfile_prefix_chars='@')
    parser.add_argument('--name', default='mindmap')
    parser.add_argument('--default-img-size', default='80,43')
    parser.add_argument('--shrink', action='store_true')
    parser.add_argument('--no-shrinking-edges', action='store_false', dest='shrinking_edges')
    parser.add_argument('--palette', choices=list(PALETTES.keys()) + ['none'], default='dark-solarized')
    parser.add_argument('--font-color', default='white')
    parser.add_argument('input_filepath')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main()
