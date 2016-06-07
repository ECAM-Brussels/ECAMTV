#!/usr/bin/env python3
# Author: Sébastien Combéfis
# Author: Tom Selleslagh
# Version: June 7, 2016

import json
import os

from bottle import *

# Global configuration variables
PORT = int(os.environ.get('PORT', 5000))
HOST = '0.0.0.0'

# Generic route for static files
@route('/<rep:re:(css|js|images|files)>/<filename>')
def get_static_file(rep, filename):
    return static_file(filename, root='./static/' + rep)

# Generic route for files from modules
@route('/modules/<name>/<file>')
def get_module_asset(name, file):
    return static_file(file, root='./modules/{}'.format(name))

def loadmodules(modules):
    assets = {'js': [], 'css': []}
    for module in modules:
        path = 'modules/{}'.format(module)
        if os.path.isdir(path):
            for entry in os.listdir(path):
                (name, ext) = os.path.splitext(entry)
                if ext == '.css':
                    assets['css'].append('{}/{}'.format(path, entry))
                elif ext == '.js':
                    assets['js'].append('{}/{}'.format(path, entry))
    return assets

# Main page
@route('/')
def main():
    assets = loadmodules(['datetime', 'weather', 'transport', 'warning', 'logo'])
    import modules.datetime.datetime
    d = modules.datetime.datetime.DateTime().widget()
    import modules.weather.weather
    we = modules.weather.weather.Weather().widget()
    import modules.transport.transport
    t = modules.transport.transport.Transport().widget()
    import modules.warning.warning
    wa = modules.warning.warning.Warning().widget()
    import modules.logo.logo
    l = modules.logo.logo.Logo({'src': 'images/ecam-logo.png', 'alt': 'Logo ECAM'}).widget()
    import modules.filler.filler
    lf = modules.filler.filler.Filler(height=100).widget()
    return template('index.html', assets=assets, datetime=d(), weather=we(), transport=t(), warning=wa(), logo=l(), leftfiller=lf())

# Launch the server
run(host=HOST, port=PORT, debug=True)