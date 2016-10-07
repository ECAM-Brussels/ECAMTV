#!/usr/bin/env python3
# Author: Sébastien Combéfis
# Author: Tom Selleslagh
# Version: October 6, 2016

import asyncio
import importlib
import inspect
import json
import os
import queue
import sched
import threading
import time

from autobahn.asyncio.websocket import WebSocketServerFactory, WebSocketServerProtocol
from bottle import *

# Global configuration variables
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))
WS_HOST = os.environ.get('WS_HOST', '0.0.0.0')
WS_PORT = int(os.environ.get('WS_PORT', 8080))
WS_HOSTNAME = os.environ.get('WS_HOSTNAME', 'localhost')

# Global application variables
sched = sched.scheduler(time.time, time.sleep)
queue = queue.Queue()
clients = set()


# ******************************************************************************
# Initialise all the modules of the application
# ******************************************************************************
def loadmodules(modules):
    def refresh(label, widget, refreshrate):
        if len(clients) > 0:
            queue.put((label, widget()))
        sched.enter(refreshrate, 1, refresh, (label, widget, refreshrate))
    assets = {'js': set(), 'css': set()}
    components = {}
    for module in modules:
        modulename = module['name']
        path = 'modules/{}'.format(modulename)
        if os.path.isdir(path):
            # Load CSS and JS files
            for entry in os.listdir(path):
                (name, ext) = os.path.splitext(entry)
                if ext in ('.css', '.js'):
                    assets[ext[1:]].add('{}/{}'.format(path, entry))
            # Load widgets and schedule automatic refresh
            mod = importlib.import_module('modules.{0}.{0}'.format(modulename))
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and name != 'Module':
                    obj = obj(module['config']) if 'config' in module else obj()
                    widget = obj.widget()
                    components[module['label']] = {
                        'object': obj,
                        'widget': widget
                    }
                    refreshrate = obj.refreshrate
                    if refreshrate is not None:
                        sched.enter(refreshrate, 1, refresh, (module['label'],
                        widget, refreshrate))
    return (assets, components)

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

# ******************************************************************************
# Configure and run the scheduler for widgets' update
# ******************************************************************************
threading.Thread(target=lambda: sched.run()).start()

def handle_update():
    while True:
        label, content = queue.get()
        msg = json.dumps({'label': label, 'content': content})
        print('>>> Sending:', msg)
        print('>>> To:', clients)
        for client in clients:
            client.sendMessage(msg.encode('utf8'), isBinary=False)

threading.Thread(target=handle_update).start()

# ******************************************************************************
# Configure and launch the update websocket server
# ******************************************************************************
class MyServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()

    def onConnect(self, request):
        print('>>> Client connecting:', request)

    def onOpen(self):
        print('>>> WebSocket connection opened.')
        clients.add(self)

    def onClose(self, wasClean, code, reason):
        print('>>> Websocket connection closed.')
        clients.remove(self)

    def onMessage(self, payload, isBinary):
        print('>>> Message received:', payload)

def launch_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    factory = WebSocketServerFactory('ws://{}:{}'.format(WS_HOSTNAME, WS_PORT))
    factory.protocol = MyServerProtocol
    coro = loop.create_server(factory, WS_HOST, WS_PORT)
    server = loop.run_until_complete(coro)
    loop.run_forever()

threading.Thread(target=launch_server).start()

# ******************************************************************************
# Configure and launch the main web server
# ******************************************************************************

# Generic route for global static files
@route('/<rep:re:(css|js|images|files)>/<filename>')
def get_static_file(rep, filename):
    return static_file(filename, root='./static/' + rep)

# Generic route for files from modules
@route('/modules/<name>/<file>')
def get_module_asset(name, file):
    return static_file(file, root='./modules/{}'.format(name))

# Main screen
@route('/')
def main():
    widgets = {}
    for label in components:
        widgets[label] = components[label]['widget']
    jsconf = '''var ws_hostname = '{}';
        var ws_port = {};'''.format(WS_HOSTNAME, WS_PORT)
    return template('index.html', assets=assets, widgets=widgets, jsconf=jsconf)

# Launch the web server
run(host=HOST, port=PORT, debug=True)