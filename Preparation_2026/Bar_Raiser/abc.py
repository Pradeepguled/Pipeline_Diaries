from collections import counter
list1 = [1,2,3,4,5,12,45,2,1,5,3,45]
freq = counter(list1)
rep = {k : v for k , v in freq.items()}
print (rep)
 
