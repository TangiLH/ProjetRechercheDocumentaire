from func import findWord
import sys
if(len(sys.argv)==1):
    print("donner un mot")
    exit(0)
findWord(sys.argv[1])