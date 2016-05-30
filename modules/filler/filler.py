# filler.py
# Author: Sébastien Combéfis
# Version: May 30, 2016

from bottle import template

from modules.module import Module

class Filler(Module):
    '''Class representing a module that just shows nothing.'''
    def __init__(self, width=None, height=None):
        super().__init__('Filler')
        self.__width = width
        self.__height = height
    
    def widget(self):
        style = ''
        if self.__width is not None:
            style += 'width: {}px;'.format(self.__width)
        if self.__height is not None:
            style += 'height: {}px;'.format(self.__height)
        def render():
            return template('./modules/filler/widget.tpl', style=style)
        return render
    
    def page(self):
        return None