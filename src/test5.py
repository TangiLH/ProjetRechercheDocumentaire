from func import loadDict
dictionnaire=loadDict()
liste=list(dictionnaire.keys())
liste.sort()

print(liste)
"""
liste=list(dictionnaire.get("the").items())
liste.sort(key=lambda tuple:tuple[1],reverse=True)
print(liste)"""