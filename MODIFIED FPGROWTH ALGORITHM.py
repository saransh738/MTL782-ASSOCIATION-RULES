#!/usr/bin/env python
# coding: utf-8

# In[1]:


from itertools import chain, combinations
import time 
from collections import defaultdict


class FPNode:
    def __init__(self,ID,ancestor,frequency):
        self.ID = ID   #id of the fpnode class item
        self.descendent = {} #child of the fpnode class item
        self.frequency = frequency #frequency of the fpnode class item
        self.Ancestor = ancestor #parent of the fpnode class item
        self.N_Link = None #link node of the fpnode class
        
def projected_Construct_FP(S_min,DataBase):
    Reference_Table = {}   
    for row in DataBase:
        for element in row:
            # if item is not in reference table, we will add it from database
            if(Reference_Table.get(element)==None): 
                Reference_Table[element]=DataBase[row]
            # if item is in reference table, we will update it using database
            else:
                Reference_Table[element] = Reference_Table.get(element) + DataBase[row]
    #now,we will delete elements having support less than minimum support
    for element in list(Reference_Table):
        if Reference_Table[element] < S_min: del(Reference_Table[element])
   # now we form frequent 1 itemset i.e. recurrent_set         
    recurrent_set = set(Reference_Table.keys())
    # if no recurrent set , return none
    n=len(recurrent_set)
    if n == 0: return None, None
    
    # now create reference table in the form of [element,{frequency,nodelink}]
    for element in Reference_Table:
        Reference_Table[element] = [Reference_Table[element], None]

 
   #############################################################333###################################    
    # now we will break database into projected database
    DBS=[]
    RTable=sorted(Reference_Table.items(),key=lambda p: p[1][0],reverse=True)
    for i in range(len(RTable)):
        element1 =RTable[i][0]
        PDB={}
        y=DataBase.copy()
        y.clear()
        y=DataBase.copy()
        for Set,freq in y.items():
            if element1 in Set:
                PDB[Set]=freq
                del(DataBase[Set])
        DBS.append(PDB)
    
        

    FTREES=[]
    RT=[]
    for i in range(len(DBS)):
        database=DBS[i]
        R_Table=Reference_Table
        # initialize fptree using null set
        FPTREE = FPNode('Null Set',None,1)
        #now,we will again scan the data second time and make the fptree
        for SET,freq in database.items():
            recurrent_items = {}
            for element in SET:
                if element in recurrent_set: recurrent_items[element] = R_Table[element][0]
            if len(recurrent_items) != 0:
                #now we will order the elements in the decreasing order of frequency count
                ordered_SET = [v[0] for v in sorted(recurrent_items.items(), key=lambda p: p[1], reverse=True)]
                # now we will update the fpTree
                SET,tree=ordered_SET,FPTREE
                n,i=len(SET),0
                while(i<n):
                    # if element is not in tree.descendent, we will make a new node for it
                    if SET[i] not in tree.descendent:
                        tree.descendent[SET[i]] = FPNode(SET[i],tree,freq)
                        if R_Table[SET[i]][1] == None: R_Table[SET[i]][1] = tree.descendent[SET[i]]
                        else:
                            Test_Node=R_Table[SET[i]][1]
                            # we will update the link node here
                            while (Test_Node.N_Link != None):
                                Test_Node = Test_Node.N_Link
                            Test_Node.N_Link = tree.descendent[SET[i]]       
                    else:
                         tree.descendent[SET[i]].frequency +=freq
                    if i!= n-1: tree=tree.descendent[SET[i]]
                    i =i+1 
        FTREES.append(FPTREE)
        RT.append(R_Table)
  #############################################################################################################                  
    return FTREES, RT

def assoRule(Set,frequency_set,minimum_confidence):
    for i in range(len(Set)):
        subsets = chain.from_iterable(combinations(Set[i],r) for r in range(1,len(Set[i])))
        itemSetSup = frequency_set[i]
        for s in subsets:
            conf = float(itemSetSup / frequency_set[Set.index(set(s))])
            if(conf > minimum_confidence):
                print("{} => {} at confidence {}".format(set(s), set(Set[i].difference(s)), conf))
    
def FP_Mine(tree, Reference_Table, S_min, pathprefix, recurrent_set,frequency_set):
    # now we will mine the given fptree
    y=sorted(Reference_Table.items(),key=lambda p: p[1][0])
     # list contain items and their frequency from the reference table
    List = [[x[0],x[1][0]] for x in y]
    for L in List:
        new_recurrentset = pathprefix.copy() # we will copy old prefix path
        new_recurrentset.add(L[0]) # add element in set
        if (new_recurrentset not in recurrent_set):
            frequency_set.append(L[1]) # add corrosponding frquency in the set
            recurrent_set.append(new_recurrentset)  
        #define new fpnode
        FPNode=Reference_Table[L[0]][1]
        cp_base = {}  # conditional_patterns_base
        #we will find prefixpath for the given element
        while FPNode != None:
            path_prefix = []
            LNode=FPNode
            while(LNode.Ancestor !=None):
                path_prefix.append(LNode.ID)
                LNode=LNode.Ancestor
            if len(path_prefix) != 1: cp_base[tuple(path_prefix[1:])] = FPNode.frequency
            FPNode = FPNode.N_Link
            # we will remove element from fptree which have support less than support minimum
        c_tree, c_header = projected_Construct_FP(S_min,cp_base)
        if c_header != None: FP_Mine(c_tree, c_header[0], S_min, new_recurrentset, recurrent_set,frequency_set)

def main(input_file,S_min):
    # now we will open our file
    with open(input_file) as file:
        DataBase = file.readlines()
    elements = [row.strip() for row in DataBase]
    Tns = []
    n=len(elements)
    
    for i in range(n): Tns.append(elements[i].split())
    Dataset = defaultdict(int)
    for row in Tns: Dataset[tuple(row)] += 1
    recurrent_set,frequency_set = [],[]     
    trees, Reference_Table = projected_Construct_FP(S_min,Dataset) #tree making
    for i in range(len(trees)):
        FP_Mine(trees[i], Reference_Table[i], S_min, set([]), recurrent_set,frequency_set)  #mining
    print("Frequent itemsets are:")
    for i in range(len(frequency_set)):
        print(" {} with frequency  {}".format(recurrent_set[i],frequency_set[i]))
    print("\n Total frequent items are {} \n".format(len(recurrent_set)))
    print("Association rules are:")
    assoRule(recurrent_set,frequency_set,0.8)


start= time.time()
main("data.txt",881)
end=time.time()
print("\n Total Time taken is {} seconds".format( end-start))


# In[ ]:




