###Tangi LE HENAFF
from __future__ import annotations
import json
import nltk


class Terme:
    def __init__(self,nom:str,nb:int,fichier:str) -> None:
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
    
    def __add__(self,val):
        return Terme(self.nom,self.nb+val,self.fichier)
    
    def __eq__(self, autre: Terme) -> bool:
        return self.nb==autre.nb
    
    def __gt__(self,autre: Terme) -> bool:
        return self.nb>autre.nb

def occurences(nomFichier:str):
    stop=open("../stopwords.txt")
    str=stop.read()
    stopList=str.splitlines()
    stop.close()
    fich=open(nomFichier,"r")
    res=open("res/res.txt","r+")
    res.truncate(0)
    chaine=fich.readline()
    listeTermes=[]
    dictionnaire=dict()
    sno = nltk.stem.SnowballStemmer('french')
    while  chaine!="":
        chaine=chaine.splitlines()
        for mot in chaine[0].split(" "):
            if mot.isalnum() and not stopList.__contains__(mot):
                #mot=mot.replace(".","")
                mot=sno.stem(mot)
                dictionnaire[mot]=dictionnaire.get(mot,Terme(mot,0,nomFichier))+1


        chaine=fich.readline()
    #dictionnaire=list(dictionnaire.items())
    print(dictionnaire)
    json.dump(list(dictionnaire.items()),res,default=vars)
    fich.close()

def termeFromDict(di:dict)->Terme:
    return Terme(di["nom"],di["nb"],di["fichier"])