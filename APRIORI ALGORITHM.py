#!/usr/bin/env python
# coding: utf-8

# In[3]:


from itertools import chain,combinations
import time
from collections import defaultdict

filename="data.txt"
sup = 881

with open(filename) as f:
    database = f.readlines()

database = [x.strip() for x in database]

T,freq_sets = [],defaultdict(int)        

for i in range(0,len(database)): T.append(database[i].split())

def apriori(L1,sup):
    k = 0
    L = [L1]
    while(len(L[k])>0):
        # self joining
        Ck_plus1 = []
        lk = len(L[k])
        for i in range(lk):
            for j in range(i+1,lk):
                if L[k][i][:k] == L[k][j][:k]:
                    a,b = min(L[k][i][k],L[k][j][k]),max(L[k][i][k],L[k][j][k])
                    Ck_plus1.append(L[k][i][:k]+[a,b])
        # pruning
        pruned_Ck_plus1 = []
        for candidate in Ck_plus1:
            k_sets = list(map(list,set(combinations(set(candidate),k+1)))) # all k subsets
            flag = 1
            for i in range(len(k_sets)):
                if list(sorted(k_sets[i])) not in L[k]: flag = 0
            if flag: pruned_Ck_plus1.append(candidate)
        
        Ck_plus1_sup = defaultdict(int)
        for item in T1:
            for item_1 in pruned_Ck_plus1:
                if (set(item_1).issubset(set(item))):
                    Ck_plus1_sup[tuple(item_1)] += 1
        Lk_plus1_new = []
        for items in Ck_plus1_sup:
            if (Ck_plus1_sup[items] >= sup):
                Lk_plus1_new.append(sorted(list(items)))
                freq_sets[tuple(sorted(list(items)))] = Ck_plus1_sup[items]
        L.append(Lk_plus1_new)
        k += 1
    return L

def assoRule(Set, minConf):
    for itemSet in Set:
        subsets = chain.from_iterable(combinations(itemSet,r) for r in range(1,len(itemSet)))
        itemSetSup = freq_sets[tuple(sorted(list(itemSet)))]
        for s in subsets:
            conf = float(itemSetSup / freq_sets[tuple(sorted(list(s)))])
            if(conf > minConf):
                print("{} => {} at confidence {}".format(set(s), set(itemSet.difference(s)), conf))

start=time.time()
C1,L1,n = defaultdict(int),[],len(T)
for i in range(n):
    for j in range(len(T[i])):
        elem = T[i][j]
        C1[elem] += 1

for elem in C1.keys():
    if C1[elem] >= sup:
        L1.append([elem])
        freq_sets[(elem,)] = C1[elem]

T1 = []
for i in range(n):
    tmp = []
    for j in range(len(T[i])):
        if [T[i][j]] in L1: tmp.append(T[i][j])
    T1.append(tmp)

L = apriori(L1,sup)
print(len(freq_sets))
 
freq_set = []
for i in range(len(L)):
    for j in range(len(L[i])):
        freq_set.append(set(L[i][j]))
assoRule(freq_set,0.8)

end=time.time()
print("\n Total Time taken is {} seconds".format( end-start))


# In[2]:


print(freq_sets)

