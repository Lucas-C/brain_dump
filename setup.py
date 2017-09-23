from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'graphviz_md2png = brain_dump.cli.graphviz_md2png:main',
            'wisemapping_md2xml = brain_dump.cli.wisemapping_md2xml:main',
            'wisemapping_wxml2xml = brain_dump.cli.wisemapping_wxml2xml:main',
        ],
    },
)
