# warning.py
# Author: Sébastien Combéfis
# Version: May 30, 2016

from bottle import template

from modules.module import Module

class Warning(Module):
    '''Class representing a module that shows a banner with warnings.'''
    def __init__(self):
        super().__init__('Warning', 3600)
    
    def widget(self):
        def render():
            data = ['Salle polyvalente fermée ce jeudi 17 décembre 2015']
            return template('./modules/warning/widget.tpl', warnings=data)
        return render
    
    def page(self):
        return None