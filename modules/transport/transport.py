# transport.py
# Author: Sébastien Combéfis
# Author: Tom Selleslagh
# Version: May 28, 2016

import urllib.request
import xml.dom.minidom

from bottle import template

from modules.module import Module

# Global configuration variables
STIB_API_URL = 'http://m.stib.be/api/getwaitingtimes.php?line={}&halt={}'
STIB_LINES = [(1, 8141), (1, 8142), (79, 2042)]

class Transport(Module):
    '''Class representing a module that shows transport schedules.'''
    def __init__(self):
        super().__init__('Transport', 3600)
    
    def widget(self):
        def _waitingtimes(data):
            fields = ('line', 'destination', 'minutes')
            infos = {}
            with xml.dom.minidom.parseString(data) as doc:
                for waitingtime in doc.documentElement.getElementsByTagName('waitingtime'):
                    (line, destination, minutes) = (waitingtime.getElementsByTagName(e)[0].firstChild.nodeValue for e in fields)
                    if line not in infos:
                        infos[line] = {}
                    if destination not in infos[line]:
                        infos[line][destination] = []
                    infos[line][destination].append(minutes)
            return infos
        def render():
            try:
                data = []
                for (line, halt) in STIB_LINES:
                    with urllib.request.urlopen(STIB_API_URL.format(line, halt), timeout=3) as response:
                        data.append(_waitingtimes(response.read().decode('utf-8')))
                return template('./modules/transport/widget.tpl', schedule=data)
            except:
                return '<div id="transport" class="widget">Schedule info not available at this time.</div>'
        return render
    
    def page(self):
        return None