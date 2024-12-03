from func import tf_idf_for_all
testDict=dict()
testDict["a"]=dict()
testDict["b"]=dict()
testDict["c"]=dict()
testDict["a"]["txt1"]=[1,[1,2,3]]
testDict["a"]["txt2"]=[3,[1,2,3]]
#testDict["a"]["txt3"]=[4,[1,2,3]]
testDict["b"]["txt1"]=[1,[1,2,3]]
testDict["b"]["txt2"]=[48,[1,2,3]]
#testDict["b"]["txt3"]=[12,[1,2,3]]
testDict["c"]["txt1"]=[48,[1,2,3]]
testDict["c"]["txt2"]=[18,[1,2,3]]
testDict["c"]["txt1"]=[4,[1,2,3]]
print(testDict)
tf_idf_for_all(testDict)
print(testDict)