###Tangi LE HENAFF
import json
import nltk
def occurences(nomFichier:str):
    fich=open(nomFichier)
    chaine=fich.readline()
    dictionnaire=dict()
    sno = nltk.stem.SnowballStemmer('french')
    while  chaine!="":
        chaine=chaine.splitlines()
        for mot in chaine[0].split(" "):
            if mot.isalnum():
                mot=sno.stem(mot)
                dictionnaire[mot]=dictionnaire.get(mot,0)+1


        chaine=fich.readline()
    dictionnaire=list(dictionnaire.items())
    print(json.dump(dictionnaire,fich))
    fich.close()
occurences("res/test1.txt")