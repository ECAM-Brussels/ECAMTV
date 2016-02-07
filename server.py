__author__ = 'DrimTim'

#Public libraries
from bottle import *
import json


#Personnal libraries
from lib.stib import Waitatstation
from lib.meteo import Weather


#Loading of the different database and Port
PORT = 8090
HOST = 'localhost'
EVENT = "./database/event.ddb"
STUDENT = "./database/students.ddb"
HORAIRE = "./database/horaire.ddb"
INFOS = "./database/infos.ddb"




#Separation of the different static files
@route('/script/<filename>')
def server_static(filename):
  return static_file(filename, root="./static/script")

@route('/img/<filename>')
def server_static(filename):
  return static_file(filename, root="./static/img")

@route('/style/<filename>')
def server_static(filename):
  return static_file(filename, root="./static/style")

@route('/pdf/<filename>')
def server_static(filename):
  return static_file(filename, root="./static/pdf")



#Route of the different parts of the website


#----- Main page----
@route('/')
def main():
    meteo = Weather()
    with open(EVENT, 'r') as dico:
            dicoevent = json.load(dico)
    return template('index.html', meteo=meteo,event=dicoevent)




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

run(host = HOST, port = PORT, debug = True)

