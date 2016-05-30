# logo.py
# Author: Sébastien Combéfis
# Version: May 30, 2016

from bottle import template

from modules.module import Module

class Logo(Module):
    '''Class representing a module that shows transport schedules.'''
    def __init__(self, logo):
        super().__init__('Logo')
        self.__logo = logo
    
    def widget(self):
        def render():
            return template('./modules/logo/widget.tpl', logo=self.__logo)
        return render
    
    def page(self):
        return None