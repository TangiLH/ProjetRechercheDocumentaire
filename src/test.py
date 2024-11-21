from func import *
occurences("res/test1.txt")
fich=open("res/res.txt","r")
liste = json.load(fich)
listeTerme=[]
print("\n")
print(liste[0][1].values())
for terme in liste:
    listeTerme.append(termeFromDict(terme[1]))
listeTerme.sort(key=lambda x:x.nb)
print(listeTerme)