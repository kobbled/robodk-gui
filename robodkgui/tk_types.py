"""
User defined types
-----------------------

These structures are used in the parse tree for organzing and storing
the json file in a usable format for :class:`creategui.tkGUI`
"""

import collections

tkvars = collections.namedtuple('tkvars', 'name label type parent')

tkdisp = collections.namedtuple('tkdisp', 'name type color parent')

tkspacer = collections.namedtuple('tkspacer', 'width height color parent')

tkframe = collections.namedtuple('tkframe', 'name parent toggle')

tkprogbar = collections.namedtuple('tkprogbar', 'name type length determinate parent')

tkradio = collections.namedtuple('tkradio', 'name type modes parent')

tktoggle = collections.namedtuple('tktoggle',
    'name type label '
    'trueframe falseframe '
    'parent'         
)

tkbutton = collections.namedtuple('tkbutton',
    'label file command '
    'font color '
    'expand fill side '
    'width height '
    'parent'         
)