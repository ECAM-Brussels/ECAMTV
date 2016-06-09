# info.py
# Author: Sébastien Combéfis
# Version: June 9, 2016

from bottle import template

from modules.module import Module

class Info(Module):
    '''Class representing a module that shows information panels.'''
    def __init__(self):
        super().__init__('Info')
    
    def widget(self):
        def render():
            data = [
                {'title': 'Formation LaTeX', 'content': '<p>Sébastien Combéfis vous introduira à <i>LaTeX</i>.</p>'},
                {'title': 'Défense des TFEs', 'content': '<p>Les étudiants de <b>2ème master</b> défendent leurs TFEs du 20 à 22 juin 2016.</p>'}
            ]
            return template('./modules/info/widget.tpl', infos=data)
        return render
    
    def page(self):
        return None