# USAGE: py.test tests/test_wisemapping_xml.py

from braindump.wisemapping_xml import topic_from_line, Topic

import pytest


@pytest.mark.parametrize(('line', 'expected_topic'), [
    ('toto', Topic(text='toto', link=None, icons=(), attrs='', id=0, see=[])),
    ('[Framindmap](https://framindmap.org)', Topic(text='Framindmap', link='https://framindmap.org', icons=(), attrs='', id=0, see=[])),
    ('![coucou](http://website.com/favicon.ico)', Topic(text='coucou', link=None, icons=(), attrs='image=":http://website.com/favicon.ico" shape="image"', id=0, see=[])),
    ('!toto', Topic(text='!toto', link=None, icons=(), attrs='', id=0, see=[])),
    ('Productivity   !icon=chart_bar <!-- fontStyle=";;#104f11;;;" bgColor="#d9b518" -->', Topic(text='Productivity', link=None, icons=('chart_bar',), attrs='bgColor="#d9b518" fontStyle=";;#104f11;;;"', id=0, see=[])),
    ('**toto**', Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;bold;;"', id=0, see=[])),
    ('__toto__', Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;;italic;"', id=0, see=[])),
    ('__**toto**__', Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;bold;italic;"', id=0, see=[])),
    ('**__toto__**', Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;bold;italic;"', id=0, see=[])),
    ('toto !icon=ahoy', Topic(text='toto', link=None, icons=('ahoy',), attrs='', id=0, see=[])),
    ('!icon=A toto !icon=B', Topic(text='toto', link=None, icons=('A', 'B'), attrs='', id=0, see=[])),
    ('![toto](http://website.com/favicon.ico 600x0400)', Topic(text='toto', link=None, icons=(), attrs='image="600x400:http://website.com/favicon.ico" shape="image"', id=0, see=[])),
    ('[x] toto', Topic(text='toto', link=None, icons=('tick_tick',), attrs='', id=0, see=[])),
    ('toto (see: "a ")', Topic(text='toto', link=None, icons=(), attrs='', id=0, see=['a'])),
    # TODO: require support for https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-decoration in mindplot/src/main/javascript/Topic.js line 356 & web2d/src/main/javascript/Text.js line 48
    ('~~toto~~', Topic(text='toto', link=None, icons=(), attrs='', id=0, see=[])),
])
def test_topic_from_line(line, expected_topic):
    assert topic_from_line(line) == expected_topic
