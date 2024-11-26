###Tangi LE HENAFF
from __future__ import annotations
import json
import nltk
import os, glob
from bs4 import BeautifulSoup #parser SGML https://stackoverflow.com/questions/4633162/sgml-parser-in-python


class Terme:
    def __init__(self,nom:str,nb:int,fichier:list) -> None:
        if(type(nom))!=str :
            raise TypeError("nom doit être une chaine de caracteres")
        if nom=="":
            raise ValueError("nom ne peut être vide")
        
        self.nom=nom
        self.nb=nb
        self.fichier=fichier
    
    def __str__(self) -> str:
        return self.nom+" ->-> "+str(self.nb)+" ("+self.fichier+")" 
    
    def __repr__(self) -> str:
        return str(self)
    
    def __add__(self,val,fichier):
        return Terme(self.nom,self.nb+val,self.fichier)
    
    def __eq__(self, autre: Terme) -> bool:
        return self.nb==autre.nb
    
    def __gt__(self,autre: Terme) -> bool:
        return self.nb>autre.nb
    
class Occurences:
    def __init__(self) -> None:
        self.dict=dict()

    def add(self,nomFichier):
        self.dict[nomFichier]=self.dict.get(nomFichier,0)+1
    
    def __str__(self) -> str:
        return str(self.dict)
    def __repr__(self):
        return str(self)

def occurences(nomFichier:str,texte:str,dictionnaire:dict,stopList:list)->dict:
    
    sno = nltk.stem.SnowballStemmer('english')
    for ligne in texte.splitlines():
        for mot in ligne.split(" "):
            mot=sno.stem(mot)
            if mot.isalnum() and not stopList.__contains__(mot):
                #mot=mot.replace(".","")
                
                terme=dictionnaire.get(mot)
                if terme==None:
                    terme=dict()
                terme[nomFichier]=terme.get(nomFichier,0)+1
                dictionnaire[mot]=terme
    return dictionnaire

def termeFromDict(di:dict)->Terme:
    return Terme(di["nom"],di["nb"],di["fichier"])

def parseFile(nomFichier:str,stopList,dictionnaire):
    fich=open(nomFichier)
    str=fich.read()
    fich.close()
    soup=BeautifulSoup(str,'html.parser')
    set=soup.find_all('doc')
    i=0
    for doc in set:
        print(doc.find('docno').text)
        i+=1
        if(doc.find('text'))!=None: 
            dictionnaire=occurences(doc.find('docno').text[1:-1],doc.find('text').text,dictionnaire,stopList)

def parseAll():
    stop=open("../stopwords.txt")
    str=stop.read()
    stopList=str.splitlines()
    stop.close()
    dictionnaire=dict()
    for filename in glob.glob('../AP/AP*'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            parseFile(filename,stopList,dictionnaire)

    dest=open("res/res.txt","r+")
    dest.truncate(0)
    json.dump(dictionnaire,dest,default=vars)

def loadDict()->dict:
    dest=open("res/res.txt","r")
    dictionnaire=json.load(dest)
    dest.close()
    return dictionnaire
    