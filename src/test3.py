from bs4 import BeautifulSoup #parser SGML https://stackoverflow.com/questions/4633162/sgml-parser-in-python
from func import *
fich=open("../AP/AP891217")
str=fich.read()
fich.close()
soup=BeautifulSoup(str,'html.parser')
set=soup.find_all('doc')
dictionnaire=dict()
stop=open("../stopwords.txt")
str=stop.read()
stopList=str.splitlines()
stop.close()
i=0
for doc in set:
    print(doc.find('docno').text)
    i+=1
    if(doc.find('text'))!=None: 
        dictionnaire=occurences(doc.find('docno').text,doc.find('text').text,dictionnaire,stopList)
print(dictionnaire)