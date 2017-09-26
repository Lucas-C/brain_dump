#!/usr/bin/python

# Asumptions:
# - the directory when this app is launched contains:
#   * a git repo
#   * a versionned `brain_dump.txt` file
# - GIT_CMD_PATH exists

# Typical use case scenario:
#   curl -v -XPOST -F Body=Foo $ENDPOINT
#   curl -v -XPOST -F Body=Foo$'\n'Bar $ENDPOINT
#   curl -v -XPOST -F Body=Foo $ENDPOINT
#   curl -v -XPOST -F Body=Foo.Foo$'\n'Bar $ENDPOINT

import cgi, html, logging, logging.handlers, os, shlex, subprocess, traceback
from contextlib import contextmanager
from threading import Lock
from brain_dump.parsers.indented_text_graph import parse as parse_text_graph
try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl

ROOT_DIR = os.getcwd()
LOG_FILE = os.path.join(ROOT_DIR, __file__.replace('.py', '.log'))
LOG_FORMAT = '%(asctime)s - %(process)s [%(levelname)s] %(filename)s %(lineno)d %(message)s'
TXT_DB_FILEPATH = os.path.join(ROOT_DIR, 'brain_dump.txt')
GIT_CMD_PATH = '/usr/bin/git'


def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024**2, backupCount=10)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    return logger

def log(msg, lvl=logging.INFO):
    with _LOGGER_LOCK:
        _LOGGER.log(lvl, msg)

_LOGGER = configure_logger()
_LOGGER_LOCK = Lock()
_TXT_DB_LOCK = Lock()
log('Starting. Txt db file: ' + TXT_DB_FILEPATH)


def application(env, start_response):
    path = env.get('PATH_INFO', '')
    method = env['REQUEST_METHOD']
    query_params = parse_query_string(env['QUERY_STRING'])
    form = pop_form(env)
    log('Handling request: {} "{}" with query_params: "{}", form: "{}"'.format(method, path, query_params, form))
    http_return_code = '200 OK'
    # pylint: disable=broad-except
    try:
        response = handle_request(method, path, query_params, form)
    except Exception:
        error_msg = traceback.format_exc()
        log('[ERROR] : {}'.format(error_msg), logging.ERROR)
        http_return_code = '500 Internal Server Error'
        response = html.escape(error_msg)
    start_response(http_return_code, [('Content-Type', 'application/xml')])
    return [wrap_in_twiml(response).encode('utf8')]

def wrap_in_twiml(msg):
    response = '<Message>' + msg + '</Message>' if msg else ''
    return '<?xml version="1.0" encoding="UTF-8"?><Response>' + response + '</Response>'

def pop_form(env):
    """
    Should be called only ONCE because reading env['wsgi.input'] will empty the stream,
    hence we pop the value
    """
    if 'wsgi.input' not in env:
        return None
    post_env = env.copy()
    post_env['QUERY_STRING'] = ''
    form = cgi.FieldStorage(
        fp=env.pop('wsgi.input'),
        environ=post_env,
        keep_blank_values=True
    )
    return {k: form[k].value for k in form}

def parse_query_string(query_string):
    qprm = dict(parse_qsl(query_string, True))
    return {k: qprm[k] for k in qprm}

def handle_request(method, path, query_params, form):
    assert method == 'POST'
    assert path == '/'
    assert not query_params
    assert 'Body' in form
    text = form['Body']
    key, new_value = text.split('\n', 1) if '\n' in text else (text, '')
    key, new_value = key.strip(), new_value.strip()
    if not new_value:  # => simple RETRIEVE request
        log('GET key="{}"'.format(key))
        current_value = db_get(key)
        if not current_value:
            current_value = 'UNDEFINED'
        log('-> ' + str(current_value))
        return key + '\n' + current_value
    log('PUT key="{}":value="{}"'.format(key, new_value))
    db_put(key, *new_value.splitlines())

def db_get(key):
    graph = read_graph_from_txt_db()
    node = get_node_with_content(graph, key)
    if node:
        return '\n'.join(child.content for child in node.children)

def db_put(key, *values):
    git('pull')
    with fetch_graph() as node:
        for key_frag in key.split('.'):
            matching_node = get_node_with_content(node, key_frag)
            if matching_node:
                node = matching_node
            else:
                node = node.add_child(key_frag)
        for value in values:
            if not get_node_with_content(node, value):
                node.add_child(value)
    git('commit', '-m', key + ': ' + '\n'.join(values), TXT_DB_FILEPATH)
    git('push')

def git(*args):
    log(subprocess.check_output((GIT_CMD_PATH,) + shlex.quote(args), stderr=subprocess.STDOUT).decode('utf8'))

@contextmanager
def fetch_graph():
    with _TXT_DB_LOCK:
        graph = read_graph_from_txt_db()
        yield graph
        write_graph_to_txt_db(graph)

def get_node_with_content(graph, content):
    return next((node for node in graph.children if node.content == content), None)

def read_graph_from_txt_db():
    with open(TXT_DB_FILEPATH, encoding='utf8') as txt_file:
        return parse_text_graph(txt_file.read())

def write_graph_to_txt_db(graph):
    with open(TXT_DB_FILEPATH, 'wb') as txt_file:
        txt_file.write(str(graph).encode('utf8'))
