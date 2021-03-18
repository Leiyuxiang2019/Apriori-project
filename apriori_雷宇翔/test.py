# -*- coding: utf-8 -*-
from apriori import Apriori, ImprovedApriori

with open('after.csv', 'r') as fp:
    lines = fp.readlines()
dataSet3=[]
for line in lines:
    line = line.rstrip()
    dataSet3.append(line.split(","))
minsup = 0.005
minconf = 0.5

if __name__ == '__main__':
    # test1
    apriori = Apriori(dataSet3, minsup, minconf)
    apriori.run()
    apriori.print_frequent_itemset()
    apriori.print_rule()

