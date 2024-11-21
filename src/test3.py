from bs4 import BeautifulSoup #parser SGML https://stackoverflow.com/questions/4633162/sgml-parser-in-python
fich=open("../AP/AP891217")
str=fich.read()
fich.close()
soup=BeautifulSoup(str,'html.parser')
print(soup.find_all('docno'))