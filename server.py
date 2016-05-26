#!/usr/bin/env python3
# Author: Sébastien Combéfis
# Author: Tom Selleslagh
# Version: May 25, 2016

import json
import os

from bottle import *

from lib.stib import Waitatstation
from lib.meteo import Weather

# Global configuration variables
PORT = int(os.environ.get('PORT', 5000))
HOST = '0.0.0.0'
EVENT = "./database/event.ddb"
STUDENT = "./database/students.ddb"
HORAIRE = "./database/horaire.ddb"
INFOS = "./database/infos.ddb"

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
    import modules.datetime.datetime
    d = modules.datetime.datetime.DateTime().widget()
    import modules.weather.weather
    w = modules.weather.weather.Weather().widget()
    meteo = Weather()
    with open(EVENT, 'r') as dico:
            dicoevent = json.load(dico)
    return template('index.html', datetime=d(), weather=w(), meteo=meteo,event=dicoevent)

@route('/metro/<line>/<stop>')
def main(line,stop):
    metro = Waitatstation(line,stop)
    return template(
                    "<label class='line num{{metro.id}}'>{{metro.id}}</label>"
                    "<label class='direction'>{{metro.destination}}</label>"
                    "<div class='time'>{{metro.time[0]}}</div>"
                    "<div class='time'>{{metro.time[1]}}</div>"

                    , metro=metro)

#------ Planning Page -------
@route('/planning')
def main():
    return template ('html/keypad.html')

@route('/planning/<matricule>')
def planning(matricule=14029):
    with open(STUDENT, 'r') as stud:
        allstudent = json.load(stud)
        student = allstudent['inscrit'][matricule]
    with open(HORAIRE, 'r') as hora:
        horaire = json.load(hora)
    return template('./html/planning.html',student=student,horaire=horaire)

#------ Student Life Page -------
@route('/info')
def main():
    with open(INFOS, 'r') as info:
        listepdf = json.load(info)
    return template('./html/infos.html',listing=listepdf)

#------ underconstruct page-------
@route('/underconstruction')
def main():
    return template('./html/underconstruct.html')

run(host=HOST, port=PORT, debug=True)