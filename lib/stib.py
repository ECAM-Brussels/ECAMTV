import requests
from xml.etree import ElementTree

class Waitatstation(object):
    def __init__(self, id,arret):
        self.__id=id
        self.__arret=arret
        self.__retrieve = requests.get('http://m.stib.be/api/getwaitingtimes.php?line={}&halt={}'.format(id,arret))
        self.__xmlsort = ElementTree.fromstring(self.__retrieve.content)
        self.__waiting = Waitatstation.pickup(self.__xmlsort)

    @classmethod
    def pickup(klass,node):
        time=[]
        for element in node:
           if element.tag=='waitingtime':
               for child in element:
                   if child.tag == 'minutes':
                       time.append(child.text)
                   elif child.tag == 'destination':
                       dest=child.text
        return(time,dest)

    @property
    def time(self):
        return self.__waiting[0]

    @property
    def destination(self):
        return self.__waiting[1]

    @property
    def id(self):
        return self.__id
