# warning.py
# Author: Sébastien Combéfis
# Version: June 7, 2016

from bottle import template

from modules.module import Module

class Warning(Module):
    '''Class representing a module that shows a banner with warnings.'''
    def __init__(self):
        super().__init__('Warning', 3600)
    
    def widget(self):
        def render():
            data = ['Salle polyvalente fermée ce jeudi 17 décembre 2015', 'Défense TFE ces lundis et mardis 12 juin']
            return template('./modules/warning/widget.tpl', warnings=data)
        return render
    
    def page(self):
        return None