__author__ = 'Tom'

import requests
import urllib
import json


class Weather():
    def __init__(self):
        self.__url = "http://www.prevision-meteo.ch/services/json/bruxelles-20"
        self.__data = json.loads(urllib.request.urlopen(self.__url).read().decode('utf-8'))
        self.__current={}
        self.__prevision=[{},{},{},{}]


    @property
    def current(self):
        for element in self.__data['current_condition']:
            if element == 'tmp':
                self.__current['temperature']= self.__data['current_condition'][element]
            elif element == 'icon_big':
                self.__current['picto']= self.__data['current_condition'][element]
            elif element =='condition':
                self.__current['condition']= self.__data['current_condition'][element]
        return self.__current


    @property
    def prevision(self):
        for i in range(4):
            self.__prevision[i]['min'] = self.__data['fcst_day_{}'.format(i+1)]['tmin']
            self.__prevision[i]['max'] = self.__data['fcst_day_{}'.format(i+1)]['tmax']
            self.__prevision[i]['picto'] = self.__data['fcst_day_{}'.format(i+1)]['icon_big']
            self.__prevision[i]['day'] = self.__data['fcst_day_{}'.format(i+1)]['day_short']
        return self.__prevision

