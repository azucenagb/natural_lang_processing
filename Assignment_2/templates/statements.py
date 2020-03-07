# File: statements.py

# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    def __init__ (self):
        self.list = []

    def add(self, stem, cat):
        x = (stem, cat)
        add(self.list, x)

    def getAll(self, cat):
        answer = []
        for it in self.list:
            if (it[1] is cat):
                answer.append(it[0])
        return answer

class FactBase:
    """stores unary and binary relational facts"""
    def __init__ (self):
        self.unaries = []
        self.binaries = []
    def addUnary(self, pred, e1):
        x = (pred, e1)
        add(self.unaries, x)
    def addBinary(self, pred, e1, e2):
        x = (pred, e1, e2)
        add(self.binaries, x)
    def queryUnary(self, pred, e1):
        x = (pred, e1)
        if x in self.unaries:
            return True
        else:
            return False
    def queryBinary(self, pred, e1, e2):
        x = (pred, e1, e2)
        if x in self.binaries:
            return True
        else:
            return False


import re
from nltk.corpus import brown


def functionVBZ():
    VBZ = []
    for x in brown.tagged_words():
        if x[1] == "VBZ":
            VBZ.append(x[0])
    return VBZ
listVBZ = functionVBZ()


def functionVB():
    VB = []
    for x in brown.tagged_words():
        if x[1] == "VB":
            VB.append(x[0])
    return VB
listVB = functionVB()

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    boolean1 = ((re.match(s[:-2] + "(?!(s|x|y|z|a|e|i|o|u))", s[:-1]) is not None) & (re.match(s[:-3] + "(?!(sh|ch))", s[:-1]) is not None)) & (s[len(s)-1] is 's')
    boolean2 = re.match("(.)*(a|e|i|o|u)ys", s) is not None
    boolean3 = (len(s)>4) & (re.match("(.)*(b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|u|v|w|x|y|z)(ies)",s) is not None)
    boolean4 = re.match("(.)(ies)", s) is not None
    boolean5 = re.match("(.)*(o|x|ch|sh|ss|zz)(es)", s) is not None
    boolean6 = re.match("(.)*(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|t|u|v|w|x|y)(se|ze)s", s) is not None
    boolean7 = s is "has"
    boolean89 = (re.match(s[:-3] + "(?!(s|x|o|i|z))", s[:-2]) is not None) & (re.match(s[:-4] + "(?!(sh|ch))", s[:-2]) is not None)
    boolean88 = (s[len(s)-1] is 's') & (s[len(s)-2] is 'e')
    booleanAll = boolean1 | boolean2 | boolean3 | boolean4 | boolean5 | boolean6 | boolean7 | (boolean88 & boolean89)


    if booleanAll:

        if boolean1 | boolean2 | boolean4 | boolean6:
            littleS = s[:-1]
        if boolean3:
            littleS =  s.replace(s[len(s)-3:], "y")
        if boolean5:
            littleS = s[:-2]
        if boolean7:
            return "have"
        if boolean88 & boolean89:
            littleS = s[:-1]
        if ((s in listVBZ) & (littleS in listVB)):
            return littleS

    else: return ""


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.

#if __name__ == "__main__":
    #lx = Lexicon()
    #lx.add('John', 'P')
    #print lx.getAll('P')
    #fb = FactBase()
    #print (verb_stem("fly") is "")
    #print verb_stem("are")
    #print verb_stem("dies")
    #fb.addUnary("duck", "John")
    #fb.addBinary("love", "John", "Mary")
    #print fb.queryUnary("duck", "John")
    #print fb.queryBinary("love", "Mary", "John")
