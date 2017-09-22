#!/usr/bin/python3

from collections import namedtuple
from itertools import count
from xml.sax.saxutils import quoteattr

from .parsers.pseudo_markdown import LineGrammar # require pyparsing

Topic = namedtuple('Topic', ('text', 'id', 'link', 'icons', 'attrs', 'see'))


def recursively_print_map(graph, args):
    print('<map name="{}" version="tango">'.format(args.name))
    topics = list(extract_and_print_topics(graph, args, height=graph.height, counter=count()))
    topics_ids_per_text = {topic.text:topic.id for topic in topics}
    for topic in topics:
        for dest_topic_text in topic.see:
            dest_id = topics_ids_per_text[dest_topic_text]
            print('<relationship srcTopicId="{}" destTopicId="{}" lineType="3" endArrow="false" startArrow="true"/>'.format(topic.id, dest_id))
    print('</map>')

def extract_and_print_topics(node, args, height, counter, indent='', branch_id=None, order=None):
    indent += '    '
    attrs = {}
    if order is None:
        attrs['central'] = 'true'
    else:
        attrs['order'] = order
        if branch_id is None:
            branch_id = order
        if args.shrink:
            attrs['shrink'] = 'true'
    topic = topic_from_line(node.content,
                            tid=next(counter),
                            edge_colors=args.palette,
                            edge_width=2+2*(height-indent.count('    ')) if args.shrinking_edges else None,
                            branch_id=branch_id,
                            default_attrs=attrs,
                            default_img_size=args.default_img_size,
                            font_color=args.font_color)
    print('{}<topic {} position="0,0" text={} id="{}">'.format(indent, topic.attrs, quoteattr(topic.text), topic.id))
    if topic.link:
        print('{}    <link url="{}" urlType="url"/>'.format(indent, topic.link))
    for icon in topic.icons:
        print('{}    <icon id="{}"/>'.format(indent, icon))
    yield topic
    for child_order, child in enumerate(node.children):
        yield from extract_and_print_topics(child, args, height=height, counter=counter, indent=indent, branch_id=branch_id, order=child_order)
    print('{}</topic>'.format(indent))

def topic_from_line(text_line, tid=0, edge_width=None, edge_colors=None, branch_id=None, default_attrs=None, default_img_size='', font_color=''):
    parsed_line = LineGrammar.parseString(text_line, parseAll=True)
    link = parsed_line.url
    attrs = {}
    if default_attrs:
        attrs.update(default_attrs)
    for key_value in parsed_line.attrs.split():
        key, value = key_value.split('=')
        attrs[key.strip()] = value.strip()[1:-1]
    if parsed_line.is_img:
        attrs['shape'] = 'image'
        img_size = '{}x{}'.format(int(parsed_line.img_width), int(parsed_line.img_height)) if parsed_line.img_width and parsed_line.img_height else default_img_size
        attrs['image'] = '{}:{}'.format(img_size, link)
        link = None
    set_font_style_attr(attrs, parsed_line, font_color)
    if branch_id is not None:
        if edge_colors:
            attrs['edgeStrokeColor'] = edge_colors[branch_id % len(edge_colors)]
        if edge_width is not None:
            attrs['edgeStrokeWidth'] = edge_width
    attrs = ' '.join('{}="{}"'.format(k, v) for k, v in sorted(attrs.items()))
    icons = tuple(parsed_line.icons)
    if parsed_line.has_checkbox:
        icons = icons + ('tick_tick' if parsed_line.is_checked else 'tick_cross',)
    see = [dest_text.strip() for dest_text in list(parsed_line.see)]
    return Topic(text=(parsed_line.text or [''])[0].strip(), id=tid, link=link or None, icons=icons, attrs=attrs, see=see)

def set_font_style_attr(attrs, parsed_line, default_font_color):
    font_size, font_family, font_color, bold, italic = '', '', '', '', ''
    if 'fontStyle' in attrs:
        font_size, font_family, font_color, bold, italic, _ = attrs['fontStyle'].split(';')
    if not font_color:
        font_color = default_font_color
    is_bold, is_italic, _ = bool(parsed_line.is_bold), bool(parsed_line.is_italic), bool(parsed_line.is_striked)
    if is_bold:
        bold = 'bold'
    if is_italic:
        italic = 'italic'
    if font_size or font_family or font_color or bold or italic:
        # cf. https://bitbucket.org/wisemapping/wisemapping-open-source/src/master/mindplot/src/main/javascript/persistence/XMLSerializer_Pela.js?at=develop&fileviewer=file-view-default#XMLSerializer_Pela.js-281
        attrs['fontStyle'] = '{};{};{};{};{};'.format(font_size, font_family, font_color, bold, italic)
