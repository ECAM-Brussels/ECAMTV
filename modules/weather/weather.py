# weather.py
# Author: Sébastien Combéfis
# Author: Tom Selleslagh
# Version: May 25, 2016

import json
import urllib

from bottle import template

from modules.module import Module

# Global configuration variables
WEATHER_API_URL = 'http://www.prevision-meteo.ch/services/json/bruxelles-20'

class Weather(Module):
    '''Class representing a module that shows current weather and forecasts.'''
    def __init__(self):
        super().__init__('Weather', 3600)
    
    def widget(self):
        def render():
            try:
                with urllib.request.urlopen(WEATHER_API_URL) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    return template('./modules/weather/widget.tpl', weather=data)
            except Exception as e:
                print('Erreur:', e)
                return 'Error'
        return render
    
    def page(self):
        return None