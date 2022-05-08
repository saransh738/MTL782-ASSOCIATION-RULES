# Apriori Algorithm Implementation 
### 1. Apriori Algorithm
Apriori is given by R. Agrawal and R. Srikant in 1994 for frequent item set mining and association rule learning. It proceeds by identifying the frequent individual items in the database and extending them to larger and larger item sets as long as those item sets appear sufficiently often.

### 2. Improvement over the usual Apriori-Algorithm (for Frequent Itemset Generation)

We have modified the Apriori algorithm to implement the AprioriTID algorithm. The difference between the two algorithms is in the step of counting the support of the candidate frequent item sets. While the Apriori algorithm makes a pass over the dataset for each candidate, AprioriTID algorithm does not use the database for counting the support of candidates after the 1st pass. In AprioriTID algorithm we use a vector containing potentially frequent k-item sets with id = TID. If c is a candidate k-itemset such that the k-1 itemset obtained by removing the last entry and the k-1 itemset obtained by removing the second to last entry both belong to the potential k-1 frequent vector with id t, then c is a k frequent itemset.

