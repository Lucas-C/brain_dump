# USAGE: py.test tests/test_pseudo_markdown_parser.py

from braindump.parsers.pseudo_markdown import LineGrammar

import pytest


@pytest.mark.parametrize('kwargs', [
    dict(line='[Framindmap](https://framindmap.org)', text='Framindmap', url='https://framindmap.org'),
    dict(line='![coucou](http://website.com/favicon.ico)', text='coucou', url='http://website.com/favicon.ico', is_img=True),
    dict(line='![](http://website.com/favicon.ico 600x0400)', text='', url='http://website.com/favicon.ico', is_img=True, img_dims=(600, 400)),
    dict(line='!toto', text='!toto'),
    dict(line='Productivity   !icon=chart_bar <!--fontStyle=";;#104f11;;;" bgColor="#d9b518"-->',
        text='Productivity', icons=('chart_bar',), attrs='fontStyle=";;#104f11;;;" bgColor="#d9b518"'),
    dict(line='**toto**', text='toto', is_bold=True),
    dict(line='__toto__', text='toto', is_italic=True),
    dict(line='__**toto**__', text='toto', is_bold=True, is_italic=True),
    dict(line='**__toto__**', text='toto', is_bold=True, is_italic=True),
    dict(line='~~toto~~', text='toto', is_striked=True),
    dict(line='toto !icon=ahoy', text='toto', icons=('ahoy',)),
    dict(line='!icon=A toto !icon=B', text='toto', icons=('A','B')),
    dict(line='[ ] toto', text='toto', has_checkbox=True, is_checked=False),
    dict(line='[x] toto', text='toto', has_checkbox=True, is_checked=True),
    dict(line='toto (see: "a\\"","b,c")', text='toto', see=['a"','b,c']),
])
def test_parser(kwargs):
    parser_assertions(**kwargs)

def parser_assertions(line, text, url='', icons=(), attrs='', is_bold=False, is_italic=False, is_striked=False, is_img=False, img_dims=None, has_checkbox=False, is_checked=False, see=''):
    parsed_line = LineGrammar.parseString(line, parseAll=True)
    print(parsed_line.dump())
    assert (parsed_line.text or [''])[0].strip() == text, parsed_line.text
    assert bool(parsed_line.is_bold) == is_bold
    assert bool(parsed_line.is_italic) == is_italic
    assert bool(parsed_line.is_striked) == is_striked
    assert parsed_line.url == url
    assert bool(parsed_line.is_img) == is_img
    if img_dims or parsed_line.img_width or parsed_line.img_height:
        assert (int(parsed_line.img_width), int(parsed_line.img_height)) == img_dims
    assert bool(parsed_line.has_checkbox) == has_checkbox
    assert bool(parsed_line.is_checked) == is_checked
    assert tuple(parsed_line.icons) == icons
    assert parsed_line.attrs == attrs
    assert list(parsed_line.see) == list(see)
