###Tangi LE HENAFF
from __future__ import annotations
import json
import nltk
import os, glob
import re #https://stackoverflow.com/questions/919056/case-insensitive-replace
from bs4 import BeautifulSoup, ResultSet #parser SGML https://stackoverflow.com/questions/4633162/sgml-parser-in-python

PATH="../AP/"

class Terme:
    """DEPRECIE
    sert à modéliser un terme
    """
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
    """DEPRECIE
        sert à modéliser le nombre d'occurences d'un mot
    """
    def __init__(self) -> None:
        self.dict=dict()

    def add(self,nomFichier):
        self.dict[nomFichier]=self.dict.get(nomFichier,0)+1
    
    def __str__(self) -> str:
        return str(self.dict)
    def __repr__(self):
        return str(self)

def occurences(nomTexte:str,texte:str,dictionnaire:dict,stopList:list)->dict:
    """retourne un dictionnaire contenant les occurences des mots d'un texte

    Args:
        nomTexte (str): le nom du fichier contenant le texte
        texte (str): le texte à analyser
        dictionnaire (dict): le dictionnaire à modifier
        stopList (list): la liste des mots à ne pas ajouter au dictionnaire

    Returns:
        dict: le dictionnaire d'occurences modifié
    """
    sno = nltk.stem.SnowballStemmer('english')
    i=0
    for ligne in texte.splitlines():
        i+=1
        for mot in ligne.split(" "):
            stem=sno.stem(mot)
            if mot.isalnum() and not stopList.__contains__(mot) and not stopList.__contains__(stem):
                #mot=mot.replace(".","")
                
                terme=dictionnaire.get(stem)
                if terme==None:
                    terme=dict()
                temp=terme.get(nomTexte,[0,list()])
                temp[0]+=1
                temp[1].append(i)
                terme[nomTexte]=temp
                dictionnaire[stem]=terme
    return dictionnaire

def termeFromDict(di:dict)->Terme:
    """DEPRECIE permet d'obtenir des termes depuis une chaine de caracteres

    Args:
        di (dict): le dictionnaire_

    Returns:
        Terme: le Terme renvoyé
    """
    return Terme(di["nom"],di["nb"],di["fichier"])

def parseFile(nomFichier:str,stopList,dictionnaire):
    """parcourt un fichier pour trouver les occurences des mots

    Args:
        nomFichier (str): le nom du fichier
        stopList (_type_): la liste des mots à ne pas inclure
        dictionnaire (_type_): le dictionnaire à modifier
    """
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
    """créée le fichier XML rest.txt contenant les occurences de tous les mots du corpus
    """
    stop=open("../stopwords.txt")
    str=stop.read()
    stopList=str.splitlines()
    stop.close()
    dictionnaire=dict()
    for filename in glob.glob(PATH+'AP*'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            parseFile(filename,stopList,dictionnaire)

    dest=open("res/res.txt","r+")
    dest.truncate(0)
    json.dump(dictionnaire,dest,default=vars)

def loadDict()->dict:
    """charge le dictionnaire contenu dans le fichier XML res.txt

    Returns:
        dict: le dictionnaire chargé
    """
    dest=open("res/res.txt","r")
    dictionnaire=json.load(dest)
    dest.close()
    return dictionnaire

def findword(word:str):
    """trouve un mot dans le corpus

    Args:
        word (str): le mot à trouver
    """
    dictionnaire=loadDict()
    sno = nltk.stem.SnowballStemmer('english')
    stem=sno.stem(word)
    occurences=dictionnaire.get(stem,None)
    if(occurences==None or len(occurences)==0):
        print("mot "+word+" non trouvé")
        return
    else:
        liste=list(occurences.items())
        liste.sort()
        for document,cle in liste:
            split=document.split("-")
            fichier=split[0]
            lecteur=open(PATH+fichier)
            soupSet=BeautifulSoup(lecteur.read(),'html.parser').find_all("doc")
            highlightInFile(word,soupSet,document,split[1],cle[1])
            """
            print("fichier "+str(fichier)+" document "+str(document)+" nombre d'occurences "+str(cle[0]))
            print("lignes :")
            for ligne in cle[1]:
                print(ligne)
                """

def highlightInText(word:str,textName:str,text:str):
    """affiche dans la console les lignes ou le terme apparaît dans le texte, avec le terme surligné

    Args:
        word (str): le mot à trouver
        textName (str): le nom du texte
        text (str): le texte
    """
    liste=text.splitlines()
    i=1
    for ligne in liste:
        if(ligne.__contains__(word)):
            ligne.replace(word,"\033[32m"+word+"\033[0m")
            print(i+" "+ligne)

        i+=1

def highlightInFile(word:str,soupSet:ResultSet,textName:str,textNumber:str,lineNumbers:list):
    """affiche dans la console les lignes ou le terme apparaît dans le fichier, avec le terme surligné

    Args:
        word (str): le mot à trouver
        fileName (str): le nom du Fichier
        textList (list) : la liste des noms de textes contenant le mot
    """
    
    i=0
    doc=(soupSet[int(textNumber)-1])
    text=(doc.find('text').text)
    split=text.splitlines()
    reg=regex(word)
    for lineNumber in lineNumbers:
        line=split[lineNumber-1]
        insensitive = re.compile(reg)
        test=insensitive.findall(line)
        for match in test:
            line=line.replace(match,"\033[32m"+match+"\033[0m")
        print(line)

def regex(word:str)->str:
    """genere une regex à partir du mot. la regex contient le mot en minisuscule, en majuscule, et avec la premiere lettre en majuscule

    Args:
        word (str): le mot

    Returns:
        str: la regex retournée
    """
    res=""
    res+=str.lower(word)
    res+="|"+str.upper(word)
    res+="|"+str.capitalize(word)
    return res
