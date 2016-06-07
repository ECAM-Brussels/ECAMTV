# info.py
# Author: Sébastien Combéfis
# Version: June 7, 2016

from bottle import template

from modules.module import Module

class Info(Module):
    '''Class representing a module that shows information panels.'''
    def __init__(self):
        super().__init__('Info')
    
    def widget(self):
        def render():
            return template('./modules/info/widget.tpl')
        return render
    
    def page(self):
        return None