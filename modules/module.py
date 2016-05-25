# module.py
# Author: Sébastien Combéfis
# Version: May 25, 2016

from abc import *

class Module(metaclass=ABCMeta):
    '''Abstract class representing a generic module.'''
    def __init__(self, name):
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    @abstractmethod
    def widget(self):
        '''Returns a function that renders the widget view of the module
        
        Pre: -
        Post: The returned value contains the HTML rendering of the widget view
              of this module or None if not supported by this module
        '''
        ...
    
    @abstractmethod
    def page(self):
        '''Returns a function that renders the page view of the module
        
        Pre: -
        Post: The returned value contains the HTML rendering of the page view
              of this module or None if not supported by this module
        '''
        ...