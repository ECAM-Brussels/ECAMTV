# module.py
# Author: Sébastien Combéfis
# Version: June 7, 2016

from abc import *
import copy

class Module(metaclass=ABCMeta):
    '''Abstract class representing a generic module.'''
    def __init__(self, name, refreshrate=None, options=None):
        '''Build a new module
        
        Pre: name != ''
             refreshrate > 0
        Post: A new instance of this is created representing a module
              with the specified 'name' and whose content must be updated
              given the 'refreshrate' (or never if set to None)
              and with the specified options
        '''
        self.__name = name
        self.__refreshrate = refreshrate
        self.__options = options
    
    @property
    def name(self):
        return self.__name
    
    @property
    def refreshrate(self):
        return self.__refreshrate
    
    @property
    def options(self):
        return copy.deepcopy(self.__options)
    
    @abstractmethod
    def widget(self):
        '''Return a function that renders the widget view of the module
        
        Pre: -
        Post: The returned value contains the HTML rendering of the widget view
              of this module or None if not supported by this module
        '''
        ...
    
    @abstractmethod
    def page(self):
        '''Return a function that renders the page view of the module
        
        Pre: -
        Post: The returned value contains the HTML rendering of the page view
              of this module or None if not supported by this module
        '''
        ...