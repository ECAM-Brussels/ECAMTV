#!/usr/bin/env python3
# Author: Sébastien Combéfis
# Author: Tom Selleslagh
# Version: June 13, 2016

import asyncio
import importlib
import inspect
import json
import os
import queue
import sched
import threading
import time

from bottle import *
import websockets

# Global configuration variables
HOST = '0.0.0.0'
WEBSERVER_PORT = int(os.environ.get('PORT', 5000))
WEBSOCKET_PORT = 8080


# Refresh a widget
def refresh(label, widget, refreshrate):
    if len(clients) > 0:
        queue.put((label, widget()))
    sched.enter(refreshrate, 1, refresh, (label, widget, refreshrate))

# Load a list of modules
def loadmodules(modules):
    assets = {'js': set(), 'css': set()}
    components = {}
    for module in modules:
        path = 'modules/{}'.format(module['name'])
        if os.path.isdir(path):
            # Load CSS and JS files
            for entry in os.listdir(path):
                (name, ext) = os.path.splitext(entry)
                if ext == '.css':
                    assets['css'].add('{}/{}'.format(path, entry))
                elif ext == '.js':
                    assets['js'].add('{}/{}'.format(path, entry))
            # Load widgets and schedule automatic refresh
            mod = importlib.import_module('modules.{0}.{0}'.format(module['name']))
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and name != 'Module':
                    obj = obj(module['config']) if 'config' in module else obj()
                    widget = obj.widget()
                    components[module['label']] = {'object': obj, 'widget': widget}
                    if obj.refreshrate is not None:
                        sched.enter(obj.refreshrate, 1, refresh, (module['label'], widget, obj.refreshrate))
    return (assets, components)

# Initialise all the modules of the application
# and launch their automatic scheduled update
sched = sched.scheduler(time.time, time.sleep)
assets, components = loadmodules([
    {'label' : 'datetime', 'name': 'datetime'},
    {'label' : 'weather', 'name': 'weather'},
    {'label' : 'transport', 'name': 'transport'},
    {'label' : 'leftfiller', 'name': 'filler', 'config': {'height': 100}},
    {'label' : 'warning', 'name': 'warning'},
    {'label' : 'info', 'name': 'info'},
    {'label' : 'logo', 'name': 'logo', 'config': {'src': 'images/ecam-logo.png', 'alt': 'Logo ECAM'}},
    {'label' : 'rightfiller', 'name': 'filler', 'config': {'height': 600}}
])
threading.Thread(target=lambda: sched.run()).start()

# Initialise the websocket server endpoint
queue = queue.Queue()
clients = set()

def launch_server():
    async def handle_websocket(websocket, path):
        print('=== Connexion received for', path)
        clients.add(websocket)
        while True:
            label, content = queue.get()
            print('Update of', label)
            msg = json.dumps({'label': label, 'content': content})
            await asyncio.wait([ws.send(msg) for ws in clients])
            print('SENT ')
    server = websockets.serve(handle_websocket, HOST, WEBSOCKET_PORT)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server)
    loop.run_forever()
threading.Thread(target=launch_server).start()

# Generic route for static files
@route('/<rep:re:(css|js|images|files)>/<filename>')
def get_static_file(rep, filename):
    return static_file(filename, root='./static/' + rep)

# Generic route for files from modules
@route('/modules/<name>/<file>')
def get_module_asset(name, file):
    return static_file(file, root='./modules/{}'.format(name))

# Main page
@route('/')
def main():
    widgets = {}
    for label in components:
        widgets[label] = components[label]['widget']
    return template('index.html', assets=assets, widgets=widgets)

# Launch the server
run(host=HOST, port=WEBSERVER_PORT, debug=True)