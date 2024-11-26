from func import findword
import sys
if(len(sys.argv)==1):
    print("donner un mot")
    exit(0)
findword(sys.argv[1])