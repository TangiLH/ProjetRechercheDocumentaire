def lam(liste,a,b):
    liste.append((a,b))
liste=[1,2,3,4]
liste2=[]
tuple_final=map(lambda a,b:liste2.append(a,b),liste,liste)
print(list(tuple_final))
print(liste2)