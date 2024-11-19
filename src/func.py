###Tangi LE HENAFF

def occurences(nomFichier:str):
    fich=open(nomFichier)
    chaine=fich.readline()
    dictionnaire=dict()
    while  chaine!="":
        chaine=chaine.splitlines()
        for mot in chaine[0].split(" "):
            if mot.isalnum():
                dictionnaire[mot]=dictionnaire.get(mot,0)+1


        chaine=fich.readline()
    dictionnaire=list(dictionnaire.items())
    print(dictionnaire)
occurences("res/test1.txt")