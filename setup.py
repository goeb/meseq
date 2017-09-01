#!/usr/bin/env python

from distutils.core import setup

setup(name='meseq',
      version='1.1',
      description='Editor of Message Sequence Diagrams',
      author='Fred Hoerni',
      author_email='fhoerni@free.fr',
      url='https://github.com/goeb/meseq',
      scripts=['meseq', 'meseqgui'],
      requires=['cairo',
                'pango',
                'pangocairo',
                'argparse',
                'Tkinter',
                'ScrolledText',
                'tkFileDialog',
                'tkMessageBox'
               ]
     )
