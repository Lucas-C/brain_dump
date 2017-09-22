# USAGE: py.test tests/test_indented_text_graph_parser.py

from brain_dump.parsers.indented_text_graph import parse as parse_graph

import pytest


@pytest.mark.parametrize('input_filepath', [
    'examples/basic.md',
    'examples/icons.md',
    'examples/welcome.md',
])
def test_parsing_file(input_filepath):
    with open(input_filepath) as txt_file:
        text = txt_file.read()
    if text[-1] == '\n':
        text = text[:-1]
    graph = parse_graph(text)
    out = [l.rstrip() for l in str(graph).splitlines()]
    expected = [l.rstrip() for l in text.splitlines()]
    from difflib import context_diff
    print('\n'.join(context_diff(expected, out)))
    assert out == expected

    text = 'A\n    1\n    2\nB\n    3\n        é'
    graph_root = parse_graph(text)
    print(graph_root)
    assert len(graph_root.children) == 2
    assert len(graph_root.children[0].children) == 2
    assert graph_root.children[0].children[0].depth == 2
    parse_graph(text + '\n')
    parse_graph('A\n    1\nB    A')
    try:
        parse_graph('')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('\n\n')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('    A')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('A\n  B')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('A\n        B')
        assert False
    except ValueError:
        pass
    print('All tests passed')
