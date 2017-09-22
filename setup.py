#!/usr/bin/env python

import io, sys
from os import path
from setuptools import setup, find_packages

version = '1.0.0'
setup_requires = []

parent_dir = path.abspath(path.dirname(__file__))

# Using .rst as long as Markdown is not properly supported by pypi/warehouse :( -> https://github.com/pypa/warehouse/issues/869
with io.open(path.join(parent_dir, 'README.rst'), encoding='utf-8') as readme_file:
    rst_readme = readme_file.read()

def md2rst(md_lines):
    'Only converts headers'
    lvl2header_char = {1: '=', 2: '-', 3: '~'}
    for md_line in md_lines:
        if md_line.startswith('#'):
            header_indent, header_text = md_line.split(' ', 1)
            yield header_text
            header_char = lvl2header_char[len(header_indent)]
            yield header_char * len(header_text)
        else:
            yield md_line

with io.open(path.join(parent_dir, 'CHANGELOG.md'), encoding='utf-8') as changelog_file:
    md_changelog = changelog_file.read()
rst_changelog = '\n'.join(md2rst(md_changelog.splitlines()))

with io.open(path.join(parent_dir, 'requirements.txt')) as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='braindump',
    description='Tools to generate mindmaps compatible from markdown-like text files, either as PNG with graphviz or as wisemapping-compatible XMLs',
    long_description=rst_readme + '\n\n' + rst_changelog,
    author='Lucas Cimon',
    author_email='lucas.cimon+pypi@@gmail.com',
    url='http://github.com/Lucas-C/braindump',
    install_requires=requirements,
    packages=find_packages(),
    version=version,
    setup_requires=setup_requires,
    zip_safe=True,  # http://peak.telecommunity.com/DevCenter/setuptools#setting-the-zip-safe-flag
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Text Processing :: Markup',
    ],
    keywords='mindmap wisemapping graph markdown graphviz parser',
    license='GPL-3.0',
    include_package_data=True,  # Active la prise en compte du fichier MANIFEST.in
    entry_points={
        'console_scripts': [
            'graphviz_md2png = braindump.cli.graphviz_md2png:main',
            'wisemapping_md2xml = braindump.cli.wisemapping_md2xml:main',
            'wisemapping_wxml2xml = braindump.cli.wisemapping_wxml2xml:main',
        ],
    },
)
