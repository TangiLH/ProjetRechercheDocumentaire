import sys
from findWord import findWordCall
from findWords import findWordsCall
from func import loadDFIDFDIct, loadDict,loadReverseDict,parseAll, DIR_PATH
def afficherAide():
    print("------------------\nUsage : entrer votre requête pour rechercher un ou plusieurs mots")
    print("/aide pour l'aide")
    print("/index pour refaire l'index")
    print("/max (n) pour définir le nombre de documents max . 0 = aucune limite")
    print("/sortie pour quitter\n--------------------")

def setMax(string,docsMax):
    tab=string.split(" ")
    if(len(tab)!=2 or not tab[1].isdigit):
        print("requete incorrecte /aide pour de l'aide")
        return docsMax
    else:
        return int(tab[1])if int(tab[1])>=0 else 1
        
def main():
    print("Lancement du programme, chargement des dictionnaires...")
    continuer=True
    docsMax=5
    dicos=dict()
    dicos["dict"]=loadDict()
    dicos["reverseDict"]=loadReverseDict()
    dicos["DFIDFdict"]=loadDFIDFDIct()
    stop=open(DIR_PATH+"/../stopwords.txt")
    str=stop.read()
    stopList=str.splitlines()
    stop.close()
    dicos["stopList"]=stopList
    print("------------------\nSystème de recherche documentaire")
    print("/aide pour l'aide\n------------------")
    while(continuer==True):
        inp=input("Requête ?\n")
        print("Requete : "+inp)
        if(len(inp)==0):
            print("requete vide")
        elif(inp=="/sortie"):
            continuer=False
        elif(inp=="/index"):
            parseAll()
            dicos["dict"]=loadDict()
            dicos["reverseDict"]=loadReverseDict()
            dicos["DFIDFdict"]=loadDFIDFDIct()
        elif(inp=="/aide"):
            afficherAide()
        elif(inp.split(" ")[0]=="/max"):
            docsMax=setMax(inp,docsMax)
        else:
            inp=inp.split(" ")
            if(len(inp)==1):
                print("-----------------------------------------------------------------\n")
                findWordCall([None,docsMax,inp[0]],dicos)
                print("-----------------------------------------------------------------\n")
            else:
                print("-----------------------------------------------------------------\n")
                findWordsCall([None,docsMax]+inp,dicos)
                print("-----------------------------------------------------------------\n")
if(__name__=='__main__'):
    sys.exit(main())