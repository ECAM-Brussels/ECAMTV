#!/usr/bin/env python3
# Author: Sébastien Combéfis
# Author: Tom Selleslagh
# Version: June 7, 2016

import importlib
import inspect
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

# Load a list of modules
def loadmodules(modules):
    assets = {'js': [], 'css': []}
    widgets = {}
    for module in modules:
        path = 'modules/{}'.format(module['name'])
        if os.path.isdir(path):
            # Load CSS and JS files
            for entry in os.listdir(path):
                (name, ext) = os.path.splitext(entry)
                if ext == '.css':
                    assets['css'].append('{}/{}'.format(path, entry))
                elif ext == '.js':
                    assets['js'].append('{}/{}'.format(path, entry))
            # Load widgets
            mod = importlib.import_module('modules.{0}.{0}'.format(module['name']))
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and name != 'Module':
                    obj = obj(module['config']) if 'config' in module else obj()
                    widgets[module['name']] = obj.widget()
    return (assets, widgets)

# Main page
@route('/')
def main():
    assets, widgets = loadmodules([
        {'name': 'datetime'},
        {'name': 'weather'},
        {'name': 'transport'},
        {'name': 'warning'},
        {'name': 'logo', 'config': {'src': 'images/ecam-logo.png', 'alt': 'Logo ECAM'}}
    ])
    import modules.filler.filler
    lf = modules.filler.filler.Filler(height=100).widget()
    return template('index.html', assets=assets, widgets=widgets, leftfiller=lf())

# Launch the server
run(host=HOST, port=PORT, debug=True)