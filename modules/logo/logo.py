# logo.py
# Author: Sébastien Combéfis
# Version: June 7, 2016

from bottle import template

from modules.module import Module

class Logo(Module):
    '''Class representing a module that shows transport schedules.'''
    def __init__(self, options):
        super().__init__('Logo', options=options)
    
    def widget(self):
        def render():
            return template('./modules/logo/widget.tpl', logo=self.options)
        return render
    
    def page(self):
        return None