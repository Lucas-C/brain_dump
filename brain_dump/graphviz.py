#!/usr/bin/python3

# INSTALL: apt install graphviz / apt-cyg install graphviz (Cygwin)
#          pip install pydot
# -> note: this dependancy could easily be removed as generating a .dot graph from a GraphNode
#          and calling twopi should be straightfoward, and allow to display stderr warnings like 'Pango-WARNING **: failed to choose a font, expect ugly output'
# CYGWIN: I had an issue where symptoms were: no characaters rendered, only squares; a Pango-WARNING in twopi stderr; fc-list output empty
# -> solution was to configure fontconfig to use the Windows fonts:
#         apt-cyg install xorg-x11-fonts-Type1 fontconfig
#         cat <<EOF >/etc/fonts/local.conf
#         <?xml version="1.0"?>
#         <!DOCTYPE fontconfig SYSTEM "fonts.dtd">
#         <fontconfig>
#             <dir>/c/Windows/Fonts</dir>
#         </fontconfig>
#         EOF
#         fc-cache --verbose
#         fc-list
# POTENTIAL EXTRA FEATURES: support for basic bold/italic Markdown markup: http://stackoverflow.com/a/30200953/636849

import locale, pydot, sys
from .parsers.indented_text_graph import parse as parse_text_graph


def create_solarized_mindmap_img(input_filepath, layout='twopi', font='arial', hide_branches_from_id=None, gen_dot_file=False, root_label=None):
    assert locale.getdefaultlocale()[1] == 'UTF-8' # needed to print 'Duplicate content' warning without error and to bypass pydot Dot.write default raw formatting on line 1769
    with open(input_filepath) as txt_file:
        text = txt_file.read()
    outfile_basename = input_filepath.rsplit('.', 1)[0]
    theme = DarkSolarizedTheme(layout=layout, font=font)
    graph = parse_text_graph(text, root_label=root_label)
    create_mindmap(graph, outfile_basename, theme=theme, hide_branches_from_id=hide_branches_from_id, gen_dot_file=gen_dot_file)

def create_mindmap(graph, outfile_basename, theme, hide_branches_from_id=None, gen_dot_file=False):
    graph_height = graph.height
    pygraph = pydot.Dot(root=graph.content, **theme.graph_style)
    for node in graph:
        content = pydot.quote_if_necessary(node.content) # avoid erroneous pydot 'port' detection + workaround this: https://github.com/erocarrera/pydot/issues/187
        pygraph.add_node(pydot.Node(content, **theme.node_style(node, graph_height, hide_branches_from_id)))
        if node.parent:
            parent_content = node.parent.content if ':' not in node.parent.content else '"{}"'.format(node.parent.content)
            pygraph.add_edge(pydot.Edge(parent_content, content, **theme.edge_style(node, graph_height, hide_branches_from_id)))
    if gen_dot_file:
        dot_outfile = '{}.dot'.format(outfile_basename)
        print('Generating', dot_outfile, file=sys.stderr)
        pygraph.write(dot_outfile, prog='twopi')
    png_outfile = '{}.png'.format(outfile_basename)
    print('Generating', png_outfile, file=sys.stderr)
    pygraph.write_png(png_outfile, prog='twopi')


class DarkSolarizedTheme:
    DARKGREYBLUE = '#012b37'
    # Palette from http://ethanschoonover.com/solarized
    YELLOW = '#b58900'
    ORANGE = '#cb4b16'
    VIOLET = '#6c71c4'
    RED = '#dc323f'
    BLUE = '#268bd2'
    MAGENTA = '#d33682'
    CYAN = '#2aa198'
    GREEN = '#859900'
    GREY = '#939393'

    EDGE_COLORS = [YELLOW, ORANGE, VIOLET, RED, BLUE, MAGENTA, CYAN, GREEN, GREY]

    def __init__(self, layout, font):
        self.graph_style = dict(
            layout=layout,
            overlap='false',
            splines='curved',
            fontname=font,
            bgcolor=self.DARKGREYBLUE,
        )

    def edge_style(self, dest_node, graph_height, hide_branches_from_id=None):
        color = self.graph_style['bgcolor'] if hide_branches_from_id is not None and dest_node.branch_id >= hide_branches_from_id \
                                            else self.EDGE_COLORS[dest_node.branch_id % len(self.EDGE_COLORS)]
        return dict(
            color=color,
            dir='none',
            penwidth=2 * (2 + graph_height - dest_node.depth),
        )

    def node_style(self, node, graph_height, hide_branches_from_id=None):
        color = self.graph_style['bgcolor'] if hide_branches_from_id is not None and node.branch_id >= hide_branches_from_id \
                                            else 'white'
        label = node.content.strip() if node.content and node.content != node.ROOT_DEFAULT_NAME else ''
        return dict(
            group=node.branch_id,
            shape='plaintext',
            label=label,
            fontcolor=color,
            fontsize=2 * (16 + graph_height - node.depth),
            fontname=self.graph_style['fontname'], # not inherited by default
        )
