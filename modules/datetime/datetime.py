# datetime.py
# Author: Sébastien Combéfis
# Version: May 25, 2016

from bottle import template

from modules.module import Module

class DateTime(Module):
    '''Class representing a module that shows current date and time.'''
    def __init__(self):
        super().__init__('Date and Time')
    
    def widget(self):
        def render():
            return template('./modules/datetime/widget.tpl')
        return render
    
    def page(self):
        return None