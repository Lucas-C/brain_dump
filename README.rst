|pypi_version_img| |pypi_license_img| |travis_build_status|

Tools to generate mindmaps compatible from markdown-like text files, either as PNG with graphviz or as wisemapping-compatible XMLs.

A viewer for those can be found here: https://github.com/Lucas-C/wisemapping-mindmap-viewer

Also include a [Twilio](https://www.twilio.com) webhook that can receive updates for such markdown-like mindmap files, stored in `git`.

For more information, I wrote some [blog posts](https://chezsoi.org/lucas/blog/tag/mindmap/) explaining the role of those scripts.


Table of Contents
=================

.. contents::


Usage
=====

::

    wisemapping_md2xml examples/welcome.md > welcome.xml


::

    graphviz_md2png examples/seasons.md


Deployment
==========

``upstart`` job using ``pew`` & ``uwsgi``: ``/etc/init/brain_dump.conf``

::

    start on startup

    script
        set -o errexit -o nounset -o xtrace
        cd /path/to/git/dir
        exec >> upstart-stdout.log
        exec 2>> upstart-stderr.log
        date
        APP_SCRIPT=$(dirname $(pew-in brain_dump python -c 'import brain_dump; print(brain_dump.__file__)'))/twilio_webhook_gitdb_app.py
        LANG=fr_FR.UTF-8 pew-in brain_dump uwsgi --buffer-size 8000 --http :8087 --manage-script-name --mount /webhook=$APP_SCRIPT
    end script


Changelog
=========

https://github.com/Lucas-C/brain_dump/blob/master/CHANGELOG.md


Contributing
============

::

    pip install -r dev-requirements
    pre-commit install

The 2nd command install the `pre-commit hooks <http://pre-commit.com>`__

To only execute a single unit test:

::

    py.test -k 'test_topic_from_line[toto-expected_topic0]'


.. |pypi_version_img| image:: https://img.shields.io/pypi/v/brain_dump.svg?style=flat
   :target: https://pypi.python.org/pypi/brain_dump
.. |pypi_license_img| image:: https://img.shields.io/pypi/l/brain_dump.svg?style=flat
   :target: https://pypi.python.org/pypi/brain_dump
.. |travis_build_status| image:: https://travis-ci.org/Lucas-C/brain_dump.svg?branch=master
    :target: https://travis-ci.org/Lucas-C/brain_dump
