from func import findWords
import sys
"""
if(len(sys.argv)!=3):
    print("usage : findWord.py (documentsToRetrieve (0 for all))(wordToFind)")
    exit(0)

if(not sys.argv[1].isdigit()):
    print("documentsToRetrieve must be a positive integer")
    exit(0)
if(int(sys.argv[1])<0):
    print("documentsToRetrieve must be positive or 0")
    exit(0)
    """
findWords(sys.argv[2:],int(sys.argv[1]))