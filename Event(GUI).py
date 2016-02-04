__author__ = 'Benoit'

from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import json


#global variables
lbox = None
root = None
ddb = "./database/event.ddb"


#A class to create a new information which will be display on the homepage of the server.
#Three kinds of information are available: "evenement", "changement d'horaire" and "divers".
#   @pre    the type of information has to be defined. If an existing information has to be modified its content is
#           upload in the corresponding fields otherwise they are empty.
#   @post launch a window with fields to be completed or modified by the user.
class Information:

    def __init__(self,master,type,objet="",start="",end="",titre="",date="",desc=""):

        self.master=master
        self.principalframe=ttk.Frame(master,padding=(20,20,15,15))
        self.principalframe.pack()
        self.objet=objet
        self.start=start
        self.end=end
        self.titre=titre
        self.date=date
        self.desc=desc
        self.type=type
        self.fenetreinfo(self.principalframe)

    #Create the main window
    def fenetreinfo(self,frame):

        self.n=52
        if self.type=="E":
            self.n=73

        #Subject field
        if self.objet=="":
            ttk.Label(self.principalframe,text='Objet*:').grid(row=0,sticky=W)
            self.entryobjet=ttk.Entry(self.principalframe,width=self.n)
            self.entryobjet.grid(row=0,sticky=E)
            self.entryobjet.insert(0,self.objet)
        else:
            self.l1=ttk.Label(self.principalframe,text="Objet: " + self.objet)
            self.l1.grid(row=0,sticky=W)

        #Start/End field
        framestart=ttk.Frame(frame)
        framestart.grid(row=1)
        start=ttk.Label(framestart,text='Start*:')
        start.grid(row=1,sticky=W)
        self.entrystart=ttk.Entry(framestart)
        self.entrystart.grid(row=1,column=1)
        self.entrystart.insert(0,self.start)
        end=ttk.Label(framestart,text='End*:')
        end.grid(row=1,column=2,sticky=E)
        self.entryend=ttk.Entry(framestart)
        self.entryend.grid(row=1,column=3,sticky=E)
        self.entryend.insert(0,self.end)

        #Description field
        s1 = Scrollbar(self.principalframe, orient=VERTICAL)
        s2 = Scrollbar(self.principalframe, orient=HORIZONTAL)

        #Buttons
        self.boutonannule=ttk.Button(self.principalframe,text='Annuler',command=self.master.destroy)
        self.boutonsauvegarde=ttk.Button(self.principalframe,text='Sauvegarder',command=self.sauvegarde)

        #Ajust de arrangement of the fields depending on the kind of information
        if self.type=="E":

            #Title field
            ttk.Label(self.principalframe,text='Titre*:').grid(row=2,sticky=W)
            self.entrytitre=ttk.Entry(self.principalframe,width=self.n)
            self.entrytitre.grid(row=2,sticky=E)
            self.entrytitre.insert(0,self.titre)

            #Date field
            framedate=ttk.Frame(frame)
            framedate.grid(row=3,sticky=W)
            ttk.Label(framedate,text='Date*:').grid(row=3)
            self.entrydate=ttk.Entry(framedate)
            self.entrydate.grid(row=3,column=1)
            self.entrydate.insert(0,self.date)

            #Description field
            ttk.Label(self.principalframe,text='Description:').grid(row=4,sticky=W)
            self.textdescription = Text(self.principalframe,wrap=NONE)
            self.textdescription.insert(0.0,self.desc)
            s1.config(command = self.textdescription.yview)
            s2.config(command = self.textdescription.xview)
            self.textdescription.config(yscrollcommand = s1.set, xscrollcommand = s2.set)
            self.textdescription.grid(row=4,sticky=W)
            s1.grid(column=1, row=4, sticky=W+S+N)
            s2.grid(column=0, row=5, sticky=W+E+N)

            #Buttons
            self.boutonannule.grid(row=7,sticky=W)
            self.boutonsauvegarde.grid(row=7,sticky=E)

        else:

            #Descritpion
            ttk.Label(self.principalframe,text='Description:').grid(row=2,sticky=W)
            self.textdescription = Text(self.principalframe, width=60,height=10, wrap=WORD)
            self.textdescription.insert(0.0,self.desc)
            s1.config(command = self.textdescription.yview)
            s2.config(command = self.textdescription.xview)
            self.textdescription.config(yscrollcommand = s1.set, xscrollcommand = s2.set)
            self.textdescription.grid(row=3,sticky=W)
            s1.grid(column=1, row=3, sticky=W+S+N)
            s2.grid(column=0, row=4, sticky=W+E+N)

            #Buttons
            self.boutonannule.grid(row=5,sticky=W)
            self.boutonsauvegarde.grid(row=5,sticky=E)


    #Launch a message if the essential fields are not completed
    def messagealerte(self):
        showinfo("Attention","Tous les champs notés d'une * doivent être complétés",icon='warning')


    #The following functions return the value of the respective fields
    def getobjet(self):
        if self.objet=="":
            return self.entryobjet.get().lower()
        else:
            return self.objet.lower()

    def getstart(self):
        return self.entrystart.get()

    def getend(self):
         return self.entryend.get()

    def gettitre(self):
        return self.entrytitre.get()

    def getdate(self):
        return self.entrydate.get()

    def getdescription(self):
        return self.textdescription.get('0.0',END)


    #Check the format of the date. If it's wrong, return a message depending on the fault
    def verifdate(self,date):

        decomposition=date.split('/')

        if len(decomposition)!=3:
            showinfo("Format de la date","Le format de la date doit être de la forme suivante: \n"
                                         "                 'JJ/MM/AAAA'")
            return False
        elif len(decomposition[0])!=2 or len(decomposition[1])!=2 or len(decomposition[2])!=4:
            showinfo("Format de la date","Le format de la date doit être de la forme suivante: \n"
                                         "                 'JJ/MM/AAAA'")
            return False

        for nombre in decomposition:
            try:
                int(nombre)
            except:
                showinfo("Date incorrecte","Les dates ne peuvent contenir que des nombres")
                return False

        if int(decomposition[2])<2015:
            showinfo("Date inexistante","Veuillez vérifier la validité des dates")
            return False

        mois30jours={'01','04','06','09','11'}
        mois31jours={'03','05','07','08','10','12'}
        fevrier={'02'}

        if decomposition[1] in mois30jours:
            if int(decomposition[0])>30 or int(decomposition[0])<1:
                showinfo("Date inexistante","Veuillez vérifier la validité des dates")
                return False
        elif decomposition[1] in mois31jours:
            if int(decomposition[0])>31 or int(decomposition[0])<1:
                showinfo("Date inexistante","Veuillez vérifier la validité des dates")
                return False
        elif decomposition[1] in fevrier:
            if int(decomposition[0])>28 or int(decomposition[0])<1:
                showinfo("Date inexistante","Veuillez vérifier la validité des dates")
                return False

        return True


    #Compare two dates to check if start is before end.
    def comparedate(self,datestart,dateend):

        datestart=datestart.split('/')
        dateend=dateend.split('/')

        if datestart[2]>dateend[2]:
            return False
        elif datestart[2]==dateend[2]:
            if datestart[1]>dateend[1]:
                return False
            elif datestart[1]==dateend[1]:
                if datestart[0]>dateend[0]:
                    return False

        return True


    #Define the action of the "Sauvegarde" button. If the fields have been rightly completed the content
    #of the information will be stored in a dictionary and then converted to a Json file.
    #Otherwise the user will be able to correct his faults.
    def sauvegarde(self):

        self.dico={}
        self.dico["objet"]=self.getobjet()
        self.dico["start"]=self.getstart()
        self.dico["end"]=self.getend()
        self.dico["type"]=self.type

        if self.type=='E':
            self.dico["titre"]=self.gettitre()
            self.dico["date"]=self.getdate()

        #Chek if the essential fields denoted by a '*' are completed
        for champ in self.dico:
            if self.dico[champ]=="":
                self.messagealerte()
                return False

        self.dates=[self.getstart(),self.getend()]
        if type=='E':
            self.dates.append(self.getdate())
        for date in self.dates:
            if not self.verifdate(date):
                return False

        if not self.comparedate(self.getstart(),self.getend()):
            showinfo("Dates incompatibles","La date 'Start' doit être antérieure\nà la date 'End'")
            return False

        self.dico["description"]=self.getdescription()

        #Update de Json file containing the active information by adding this new one
        try:
            with open(ddb,'r') as fileinput:
              oldsave = json.load(fileinput)
              oldsave[self.getobjet()]=self.dico
            with open(ddb,'w') as fileoutput:
              fileoutput.write(json.dumps(oldsave))
              self.master.destroy()
            listebox()
        except IOError:
            print("erreur d'ouverture de fichier")



#Define the action of the "Ajouter" button. Depending on the value of the radiobutton it will
#create the right instance of the information class.
def boutonajout(val):

    root1=Tk()
    root1.wm_title("Nouvelle information")
    if(val=="E"):
        Information(root1,"E")
    elif(val=="H"):
        Information(root1,"D")
    else:
        Information(root1,"H")


#Show the content of the selected information.
def afficher(infoobjet):

    window=Tk()
    window.wm_title(infoobjet)
    frame=ttk.Frame(window, padding=(20,20,20,20))
    frame.grid(column=0, row=0, sticky=(N,W,E,S))

    #Research the selected information in the Json file and store its content in a dictionary
    with open(ddb,'r') as dico:
            dicoinformations=json.load(dico)
            information={}
            for element in dicoinformations:
                if element==infoobjet:
                    for contenu in dicoinformations[infoobjet]:
                       information[contenu]=dicoinformations[infoobjet][contenu]

    objet=ttk.Label(frame,text="OBJET:   {}".format(information["objet"]))
    objet.grid(row=0,column=0,sticky=W)
    start=ttk.Label(frame, text="START:   {}".format(information["start"]))
    start.grid(row=1,column=0,sticky=W)
    end=ttk.Label(frame, text="END:   {}".format(information["end"]))
    end.grid(row=1,column=1,sticky=W)

    if information["type"]=='E':
        titre=ttk.Label(frame, text="TITRE:   {}".format(information["titre"]))
        titre.grid(row=2,column=0,sticky=W)
        date=ttk.Label(frame, text="DATE:   {}".format(information["date"]))
        date.grid(row=3,column=0,sticky=W)
        desc=ttk.Label(frame, text="DESCRIPTION:\n\n {}".format(information["description"]))
        desc.grid(row=4,column=0,sticky=W)
        bouton=ttk.Button(frame,text="Fermer",command=window.destroy)
        bouton.grid(row=5,column=1,sticky=E)
    else:
        desc=ttk.Label(frame, text="DESCRIPTION:\n   {}".format(information["description"]))
        desc.grid(row=2,column=0,sticky=W)
        bouton=ttk.Button(frame,text="Fermer",command=window.destroy)
        bouton.grid(row=3,column=1,sticky=E)


#Allows the user to modify an existing information by creating an instance of the information class with prefilled fields
def modification(infoobjet):

    try:
        with open(ddb,'r') as dico:
            dicoinformations=json.load(dico)
            information={}
            for element in dicoinformations:
                if element==infoobjet:
                    for contenu in dicoinformations[infoobjet]:
                       information[contenu]=dicoinformations[infoobjet][contenu]

        mastermodif=Tk()

        if information["type"]=="E":
            Information(mastermodif,type=information["type"],objet=information["objet"],start=information["start"],end=information["end"],
                        titre=information["titre"],date=information["date"],desc=information["description"])                                     #ATTENTION IMAGE
            mastermodif.wm_title("Information: évènement")
        elif information["type"]=="D":
            Information(mastermodif,type=information["type"],objet=information["objet"],start=information["start"],
                        end=information["end"],desc=information["description"])
            mastermodif.wm_title("Information: Divers")
        else:
            Information(mastermodif,type=information["type"],objet=information["objet"],start=information["start"],
                        end=information["end"],desc=information["description"])
            mastermodif.wm_title("Information: Divers")

        mastermodif.mainloop()

    except IOError:
             print("erreur d'ouverture de fichier")


#Delete the selected information
def supprimer(infoobjet):

    answer=askquestion("Attention","Etes-vous sûrs de vouloir supprimer \"{}\"".format(infoobjet),icon='question')

    if answer=='yes':
        with open(ddb,'r') as dico:
                dicoinformations=json.load(dico)
                information={}
                for element in dicoinformations:
                  if element==infoobjet:
                      for contenu in dicoinformations[infoobjet]:
                          information[contenu]=dicoinformations[infoobjet][contenu]

        del(dicoinformations[infoobjet])
        with open(ddb,'w') as fileoutput:
            fileoutput.write(json.dumps(dicoinformations))
        listebox()
    else:
        pass


#Create the menu with the previous options related to the information
def menu(master,infoobjet):

    objet=infoobjet
    menuclic = Menu(master)
    filemenu = Menu (menuclic)
    filemenu.add_command(label="Afficher", command=lambda :afficher(objet))
    filemenu.add_command(label="Modifier", command=lambda:modification(objet))
    filemenu.add_command(label="Supprimer", command=lambda :supprimer(objet))
    menuclic.add_cascade(label="Options",menu = filemenu)
    master.config(menu = menuclic)


#Create a list with the information present in the Json file
def listobjets():

    with open(ddb,'r') as dico:
        dicoinformations=json.load(dico)
        listeobjets=[]
        for element in dicoinformations:
             listeobjets.append(element.lower())
        listeobjets.sort()

    return listeobjets


#Display the subjects of the information which are in the previous list
def listebox():

    global lbox
    global root
    lbox.delete(0,END)
    for i in listobjets():
        lbox.insert(END, i)
    lbox.bind("<Double-1>", lambda event: menu(root,lbox.get(ACTIVE)))
    lbox.bind('<<ListboxSelect>>')
    for i in range(0,len(listobjets()),2):
        lbox.itemconfigure(i, background='#f0f0ff')


#Create the main window.
def listeInfosActives():

    global lbox
    global root

    root = Tk()
    root.wm_title("Liste des informations actives")

    mode = StringVar()
    mode.set("E")
    c = ttk.Frame(root, padding=(5, 5, 12, 5))
    c.grid(column=0, row=0, sticky=(N,W,E,S))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0,weight=1)

    lbox = Listbox(c,height=5,width=30,borderwidth=2, relief=GROOVE)
    listebox()

    lbl = ttk.Label(c, text="Ajout d'une nouvelle information:")
    g1 = ttk.Radiobutton(c, text="Evenement", variable=mode, value='E')
    g2 = ttk.Radiobutton(c, text="Changement d'horaire", variable=mode, value='H')
    g3 = ttk.Radiobutton(c, text="Divers", variable=mode, value='D')
    send = ttk.Button(c, text="Ajouter", command=lambda:boutonajout(mode.get()))

    lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
    lbl.grid(column=2, row=0, padx=10, pady=5)
    g1.grid(column=2, row=1, sticky=W, padx=20)
    g2.grid(column=2, row=2, sticky=W, padx=20)
    g3.grid(column=2, row=3, sticky=W, padx=20)
    send.grid(column=3, row=4, sticky=E)
    c.grid_columnconfigure(0, weight=1)
    c.grid_rowconfigure(5, weight=1)
    lbox.bind('<<ListboxSelect>>')

    #Set the color of the elements in the listebox
    for i in range(0,len(listobjets()),2):
        lbox.itemconfigure(i, background='#f0f0ff')

    #Initialise the selection of the radiobutton
    lbox.selection_set(0)

    root.mainloop()


#Launch the program
listeInfosActives()
