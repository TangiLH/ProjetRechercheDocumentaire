from func import findWords,loadDFIDFDIct,loadDict,loadReverseDict
import sys

def findWordsCall(args,dicos):
    findWords(args[2:],int(args[1]),dicos)
def main():
    if(len(sys.argv)<3):
        print("usage : findWords.py (documentsToRetrieve (0 for all))(wordToFind)")
        exit(0)

    if(not sys.argv[1].isdigit()):
        print("documentsToRetrieve must be a positive integer")
        exit(0)
    if(int(sys.argv[1])<0):
        print("documentsToRetrieve must be positive or 0")
        exit(0)
    dicos=dict()
    dicos["dict"]=loadDict()
    dicos["reverseDict"]=loadReverseDict()
    dicos["DFIDFdict"]=loadDFIDFDIct()
    stop=open("../stopwords.txt")
    str=stop.read()
    stopList=str.splitlines()
    stop.close()
    dicos["stopList"]=stopList
    findWordsCall(sys.argv,dicos)

if __name__ == '__main__':
    sys.exit(main())

