from func import findWord,highlightAllOccurences,loadReverseDict,loadDict,loadDFIDFDIct
import sys
def findWordCall(args,dicos):
    
    liste=findWord(args[2],int(args[1]),dicos)
    if liste is not None :
        highlightAllOccurences(liste,[args[2]])

def main():
    if(len(sys.argv)!=3):
            print("usage : findWord.py (documentsToRetrieve (0 for all))(wordToFind)")
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
    findWordCall(sys.argv,dicos)

if __name__ == '__main__':
    sys.exit(main())