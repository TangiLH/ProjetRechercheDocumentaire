###Tangi LE HENAFF
from __future__ import annotations
import json
import math
import string
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
            
            mot=mot.translate(str.maketrans('', '', string.punctuation))
            stem=sno.stem(mot)
            if mot.isalnum() and not stopList.__contains__(mot) and not stopList.__contains__(stem):
                
                
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
        print("parsing"+doc.find('docno').text)
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
    tf_idf_for_all(dictionnaire)
    dest=open("res/res.txt","r+")
    dest.truncate(0)
    print("writing to file")
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

def findWord(word:str,nb:int)->list:
    """trouve un mot dans le corpus

    Args:
        word (str): le mot à trouver
        nb (int): le nombre de documents à remonter
    Returns:
        list: la liste des occurences du mot
    """
    

    dictionnaire=loadDict()
    sno = nltk.stem.SnowballStemmer('english')
    stem=sno.stem(word)
    occurences=dictionnaire.get(stem,None)
    if(occurences==None or len(occurences)==0):
        print("mot "+word+" non trouvé")
        return None
    else:
        if nb==0:
            nb=len(occurences)
        sorted_occ=dict(sorted(occurences.items(), key=lambda item: item[1]))
        if(nb>len(sorted_occ)):
            nb=len(sorted_occ)
        liste=list(sorted_occ.items())[len(sorted_occ)-nb:]
        liste.reverse()
        return liste
        """
        for document,cle in liste:
            split=document.split("-")
            fichier=split[0]
            if(fichier!=memFichier or soupSet==None):
                lecteur=open(PATH+fichier)
                soupSet=BeautifulSoup(lecteur.read(),'html.parser').find_all("doc")
                lecteur.close()
            highlightInFile([stem],soupSet,document,split[1],cle[1])"""

def highlightAllOccurences(liste:list,word:str):
    """surligne toutes les occurences du mot dans le corpus

    Args:
        liste (list): la liste des occurences du mot
        word (str): le mot à surligner
    """
    sno = nltk.stem.SnowballStemmer('english')
    stem=sno.stem(word)
    memFichier=""
    soupSet=None
    for document,cle in liste:
            split=document.split("-")
            fichier=split[0]
            if(fichier!=memFichier or soupSet==None):
                lecteur=open(PATH+fichier)
                soupSet=BeautifulSoup(lecteur.read(),'html.parser').find_all("doc")
                lecteur.close()
            highlightInFile([stem],soupSet,document,split[1],cle[1])

def highlightInFile(words:list, soupSet:ResultSet,textName:str,textNumber:str,lineNumbers:list):
    """affiche dans la console les lignes ou les termes apparaissent dans le fichier, avec le terme surligné

    Args:
        words (list): les mot à trouver
        fileName (str): le nom du Fichier
        textList (list) : la liste des noms de textes contenant les mots
    """
    print("document "+textName)
    i=0
    doc=(soupSet[int(textNumber)-1])
    text=(doc.find('text').text)
    split=text.splitlines()
    regexes=list()
    for word in words:
        regexes.append(regex(word))
    for lineNumber in lineNumbers:
        line=split[lineNumber-1]
        for reg in regexes:
            insensitive = re.compile(reg)
            matches=insensitive.findall(line)
            for match in matches:
                line=line.replace(match,"\033[32m"+match+"\033[0m")
        print("("+str(lineNumber)+") "+line)

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

def findWords(words:list,nb:int):
    """surligne toutes les occurences des mots de la liste, en appliquant un ET logique aux textes

    Args:
        words (list): la liste des mots à trouver
        nb (int): le nombre de documents à remonter
    """
    liste=list()
    for word in words:
        res=findWord(word,0)
        liste.append([word,res]) #ajout de toutes les occurences des mots à une liste
    
    liste2=list()
    i=0
    for occ in liste:
        liste2.append([])
        for doc in occ[1]:
            liste2[i].append(doc[0])
    i+=1
    print(liste2)

    return

def idf_calc(N:int,df:int)->int:
    """calcule l'idf d'un terme

    Args:
        N (int): nombre de documents total
        df (int): nombre de documents où le terme apparaît

    Returns:
        int: l'idf du terme
    """
    return math.log(N/df,10)

def tf_calc(n:int)->int:
    """calcule la frequence d'un terme

    Args:
        n (int): le nombre d'occurences du terme

    Returns:
        int: la frequence du terme
    """
    return 1+math.log(n)

def tf_idf_for_all(index:dict)->dict:
    """calcule le tf_idf de tous les termes de l'index et les ajoute au dictionnaire

    Args:
        index (dict): l'index

    Returns:
        dict: l'index modifié
    """
    nbDoc=len(index)
    for terme in index:
        print("calculating tf-idf for "+terme)
        df=len(index[terme])
        idf=idf_calc(nbDoc,df)
        for document in index[terme]:
            tf_idf=idf*tf_calc(index[terme][document][0])
            index[terme][document].append(tf_idf)
    return index

