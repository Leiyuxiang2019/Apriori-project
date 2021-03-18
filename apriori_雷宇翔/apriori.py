# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import combinations
from sys import stdout




class Apriori:
    def __init__(self, transaction_list, minsup, minconf, selected_items=None):
        self.transaction_list = transaction_list
        self.transaction_list_full_length = len(transaction_list)
        self.minsup = minsup
        self.minconf = minconf
        if selected_items is not None and selected_items is not []:
            self.selected_items = frozenset(selected_items)
        else:
            self.selected_items = None

        self.frequent_itemset = dict()
        # support for every frequent itemset
        self.frequent_itemset_support = defaultdict(float)
        # convert transaction_list
        self.transaction_list = list([frozenset(transaction) \
            for transaction in transaction_list])

        self.rule = []

    def run(self):

        self.generate_frequent_itemset()
        self._after_generate_frequent_itemset()
        self.generate_rule()


    def set_selected_items(self, selected_items):
        self.selected_items = frozenset(selected_items)


    def items(self):
        items = set()
        for transaction in self.transaction_list:
            for item in transaction:
                items.add(item)
        return items

    def filter_with_minsup(self, itemsets):
        local_counter = defaultdict(int)
        for itemset in itemsets:
            for transaction in self.transaction_list:
                if itemset.issubset(transaction):
                    local_counter[itemset] += 1
        # filter with counter
        result = set()
        for itemset, count in local_counter.items():
            support = float(count) / self.transaction_list_full_length
            if support >= self.minsup:
                result.add(itemset)
                self.frequent_itemset_support[itemset] = support
        return result

    def _after_generate_frequent_itemset(self):
        if self.selected_items is None:
            return
        local_remove = []
        for key, val in self.frequent_itemset.items():
            for itemset in val:
                if not self.selected_items.issubset(itemset):
                    local_remove.append((key, itemset))
        for (key, itemset) in local_remove:
            self.frequent_itemset[key].remove(itemset)

    def generate_frequent_itemset(self):

        def _apriori_gen(itemset, length):
            # simply use F(k-1) x F(k-1) (itemset + itemset)
            return set([x.union(y) for x in itemset for y in itemset \
                if len(x.union(y)) == length])

        k = 1
        current_itemset = set()
        # generate 1-frequnt_itemset
        for item in self.items():
            current_itemset.add(frozenset([item]))
        self.frequent_itemset[k] = self.filter_with_minsup(current_itemset)
        # generate k-frequent_itemset
        while True:
            k += 1
            current_itemset = _apriori_gen(current_itemset, k)
            current_itemset = self.filter_with_minsup(current_itemset)
            if current_itemset != set([]):
                self.frequent_itemset[k] = current_itemset
            else:
                break
        return self.frequent_itemset

    def _generate_rule(self, itemset, frequent_itemset_k):

        if len(itemset) < 2:
            return
        for element in combinations(list(itemset), 1):
            rule_head = itemset - frozenset(element)
            confidence = self.frequent_itemset_support[frequent_itemset_k]/self.frequent_itemset_support[rule_head]
            if confidence >= self.minconf:
                rule = ((rule_head, itemset - rule_head), confidence)
                # if rule not in self.rule, add and recall _generate_rule() in DFS
                if rule not in self.rule:
                    self.rule.append(rule);
                    self._generate_rule(rule_head, frequent_itemset_k)

    def generate_rule(self):

        if len(self.frequent_itemset) == 0:
            self.generate_frequent_itemset()

        for key, val in self.frequent_itemset.items():
            if key == 1:
                continue
            for itemset in val:
                self._generate_rule(itemset, itemset)
        return self.rule

    def print_frequent_itemset(self):
        x1=0
        x2=0
        x3=0
        print('======================================================\n')
        print('Frequent itemset:\n')
        for key, val in self.frequent_itemset.items():
            #stdout.write('frequent itemset size of {0}:\n'.format(key))
            for itemset in val:
                if len(itemset)==1:
                    x1+=1
                if len(itemset)==2:
                    x2+=1
                if len(itemset)==3:
                    x3+=1
                print(itemset)
                print(' \n support = '+str(format(round(self.frequent_itemset_support[itemset], 3)))+'\n')
        x2+=1
        print(x1, x2, x3)
        print('======================================================\n')

    def print_rule(self):

        print('======================================================\n')
        print('Rules:\n')
        x=0
        for rule in self.rule:
          head = rule[0][0]
          tail = rule[0][1]
          if(len(head)+len(tail)<=3):
            x+=1
            confidence = rule[1]
            print(head)
            print(' ==> ')
            print(tail)
            print(' \nconfidence ='+format(round(confidence, 3))+'\n')
        print('======================================================\n')
        print('共'+str(x)+'条规则')


class ImprovedApriori(Apriori):

    def filter_with_minsup(self, itemsets):

        for itemset in itemsets:
            k = len(itemset)
            break
        local_counter = defaultdict(int)
        for transaction in self.transaction_list:
            for itemset in combinations(list(transaction), k):
                if frozenset(itemset) in itemsets:
                    local_counter[frozenset(itemset)] += 1
        # filter with counter
        result = set()
        for itemset, count in local_counter.items():
            support = float(count) / self.transaction_list_full_length
            if support >= self.minsup:
                result.add(itemset)
                self.frequent_itemset_support[itemset] = support
        return result
