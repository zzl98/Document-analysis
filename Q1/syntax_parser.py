import json
import numpy as np
from collections import defaultdict


class RuleWriter(object):
    """
    This class is for writing rules in a format 
    the judging software can read
    Usage might look like this:

    rule_writer = RuleWriter()
    for lhs, rhs, prob in out_rules:
        rule_writer.add_rule(lhs, rhs, prob)
    rule_writer.write_rules()

    """
    def __init__(self):
        self.rules = []

    def add_rule(self, lhs, rhs, prob):
        """Add a rule to the list of rules
        Does some checking to make sure you are using the correct format.

        Args:
            lhs (str): The left hand side of the rule as a string
            rhs (Iterable(str)): The right hand side of the rule. 
                Accepts an iterable (such as a list or tuple) of strings.
            prob (float): The conditional probability of the rule.
        """
        assert isinstance(lhs, str)
        assert isinstance(rhs, list) or isinstance(rhs, tuple)
        assert not isinstance(rhs, str)
        nrhs = []
        for cl in rhs:
            assert isinstance(cl, str)
            nrhs.append(cl)
        assert isinstance(prob, float)

        self.rules.append((lhs, nrhs, prob))

        
    def write_rules(self, filename="q1.json"):
        """Write the rules to an output file.

        Args:
            filename (str, optional): Where to output the rules. Defaults to "q1.json".
        """
        json.dump(self.rules, open(filename, "w"))


# load the parsed sentences
psents = json.load(open("parsed_sents_list.json", "r"))
#psents = [['A', ['B', ['C', 'blue']], ['B', 'cat']]] # test case

# print a few parsed sentences
# NOTE: you can remove this if you like
'''
for sent in psents[:10]:
    print(sent)
'''

# TODO: estimate the conditional probabilities of the rules in the grammar
out_rules_count = []

def input_rules(s):
    if isinstance(s[1],list):
        judge = 0
        newRule = []
        nodes = []
        for i in range(len(s)):
            if i == 0:
                newRule.append(s[0])
            else:
                if s[i][0] != "PUNCT":
                    nodes.append(s[i][0])
        newRule.append(nodes)
        newRule.append(1)
        
        for rule in out_rules_count:
            if newRule[0] == rule[0] and newRule[1] == rule[1]:
                judge = 1
                rule[2] += 1
                break
        if judge == 0:
            out_rules_count.append(newRule)
            
        for i in range(len(s)):
            if i != 0:
                input_rules(s[i])
        
    else:
        if s[0] != "PUNCT":
            judge = 0
            newRule = []
            newRule.append(s[0])
            word = [s[1]]
            newRule.append(word)
            newRule.append(1)
            
            for rule in out_rules_count:
                if newRule[0] == rule[0] and newRule[1] == rule[1]:
                    judge = 1
                    rule[2] += 1
                    break
            if judge == 0:
                out_rules_count.append(newRule)
           
            
'''
out_rules_count_2 = []
for i in out_rules_count:
    if i not in out_rules_count_2:
        out_rules_count_2.append(i)
'''       



type_count = []

def count_type(s):
    if isinstance(s[1],list):
        judge = 0
        newRule = []
        newRule.append(s[0])
        newRule.append(1)
        for rule in type_count:
            if newRule[0] == rule[0]:
                judge = 1
                rule[1] += 1
                break
        if judge == 0:
            type_count.append(newRule)
        for i in range(len(s)):
            if i != 0:
                count_type(s[i])
    else:
        if s[0] != "PUNCT":
            judge = 0
            newRule = []
            newRule.append(s[0])
            newRule.append(1)
            for rule in type_count:
                if newRule[0] == rule[0]:
                    judge = 1
                    rule[1] += 1
                    break
            if judge == 0:
                type_count.append(newRule)
            
for sent in psents[:10]:
    input_rules(sent)
    count_type(sent)
print("This is out_rules_count")
print(out_rules_count)
print("This is type_count")
print(type_count)



def likelihood(ruleCount,typeCount):
    for rule in ruleCount:
        key = rule[0]
        count = 0
        for t in typeCount:
            if t[0] == key:
                count = t[1]
                break
        rule[2] = rule[2]/count
        
        
likelihood(out_rules_count,type_count)
print("This is maximum-likelihood")
print(out_rules_count)


# TODO: write the rules to the correct output file using the write_rules method

rule_writer = RuleWriter()
for lhs, rhs, prob in out_rules_count:
    rule_writer.add_rule(lhs, rhs, prob)
rule_writer.write_rules()
