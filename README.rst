|pypi_version_img| |pypi_license_img| |travis_build_status|

Tools to generate mindmaps compatible from markdown-like text files, either as PNG with graphviz or as wisemapping-compatible XMLs.

A viewer for those can be found here: https://github.com/Lucas-C/wisemapping-mindmap-viewer

Also include a [Twilio](https://www.twilio.com) webhook that can receive updates for such markdown-like mindmap files, stored in `git`.

For more information, I wrote some [blog posts](https://chezsoi.org/lucas/blog/tag/mindmap/) explaining the role of those scripts.


Table of Contents
================

.. contents::


Usage
=====

::

    wisemapping_md2xml examples/welcome.md > welcome.xml


::

    graphviz_md2png examples/seasons.md


Deployment
==========

`upstart` job using `pew` & `uwsgi`: `/etc/init/braindump.conf`
```
start on startup

script
    set -o errexit -o nounset -o xtrace
    cd /path/to/braindump
    exec >> upstart-stdout.log
    exec 2>> upstart-stderr.log
    date
    LANG=fr_FR.UTF-8 HOME=$PWD pew-in brain_dump uwsgi --buffer-size 8000 --http :80 --manage-script-name --mount /webhook=braindump/twilio_webhook_gitdb_app.py
end script
```


Contributing
============

`pre-commit hooks <http://pre-commit.com>`__ installation:

::

    pip install -r dev-requirements
    pre-commit install

Unit tests (executed by `pre-commit run`):

::

    py.test


.. |pypi_version_img| image:: https://img.shields.io/pypi/v/braindump.svg?style=flat
   :target: https://pypi.python.org/pypi/braindump
.. |pypi_license_img| image:: https://img.shields.io/pypi/l/braindump.svg?style=flat
   :target: https://pypi.python.org/pypi/braindump
.. |travis_build_status| image:: https://travis-ci.org/voyages-sncf-technologies/braindump.svg?branch=master
    :target: https://travis-ci.org/voyages-sncf-technologies/braindump
