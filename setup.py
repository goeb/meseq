#!/usr/bin/env python

import setuptools

long_description = """
Meseq is a tool for generating sequence diagrams from a textual description.

Meseq has the following features:
    - generate images in formats: PNG, SVG
    - crossing messages
    - lost message
    - box of text on a life line
    - create and destroy actors
    - message to self
    - colors
    - utf-8 encoded messages
    - resolve environment variables

    More documentation here: https://goeb.github.io/meseq/
"""

setuptools.setup(
    name='meseq',
    version='2.0'
    description='Editor of Message Sequence Diagrams',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Fred Hoerni',
    author_email='fhoerni@free.fr',
    url='https://github.com/goeb/meseq',
    scripts=['meseq', 'meseqgui'],
    requires=['argparse', 'tkinter' ]
    )
