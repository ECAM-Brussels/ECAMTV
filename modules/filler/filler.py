# filler.py
# Author: Sébastien Combéfis
# Version: May 30, 2016

from bottle import template

from modules.module import Module

class Filler(Module):
    '''Class representing a module that just shows nothing.'''
    def __init__(self, options):
        super().__init__('Filler', options=options)
    
    def widget(self):
        style = ''
        if 'width' in self.options is not None:
            style += 'width: {}px;'.format(self.options['width'])
        if 'height' in self.options is not None:
            style += 'height: {}px;'.format(self.options['height'])
        def render():
            return template('./modules/filler/widget.tpl', style=style)
        return render
    
    def page(self):
        return None