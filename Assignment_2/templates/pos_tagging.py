# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    with open("sentences.txt", "r") as f:
        unchanging = []
        for line in f:
            findsingulars = re.findall('(\w{1,})(\|)(NN )', line)
            findplurals = re.findall('(\w{1,})(\|)(NNS)', line)
            singulars = []
            plurals = []
            for word in findsingulars:
                singulars.append(word[0])
            for word in findplurals:
                plurals.append(word[0])
            for word in plurals:
                if word in singulars:
                    if word not in unchanging:
                        unchanging.append(word)
        return unchanging

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):

    boolean100 = re.match("[a-z]*(men)", s) is not None
    boolean1 = ((re.match(s[:-2] + "(?!(s|x|y|z|a|e|i|o|u))", s[:-1]) is not None) & (re.match(s[:-3] + "(?!(sh|ch))", s[:-1]) is not None)) & (s[len(s)-1] is 's')
    boolean2 = re.match("[A_Z]?[a-z]*(a|e|i|o|u)ys", s) is not None
    boolean3 = (len(s)>4) & (re.match("[A-Z]?[a-z]*(b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|u|v|w|x|y|z)(ies)",s) is not None)
    boolean4 = re.match("([a-z]|[A-Z])(ies)", s) is not None
    boolean5 = re.match("[A-Z]?[a-z]*(o|x|ch|sh|ss|zz)(es)", s) is not None
    boolean6 = re.match("[A-Z]?[a-z]*(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|t|u|v|w|x|y)(se|ze)s", s) is not None
    boolean89 = (re.match(s[:-3] + "(?!(s|x|o|i|z))", s[:-2]) is not None) & (re.match(s[:-4] + "(?!(sh|ch))", s[:-2]) is not None)
    boolean88 = (s[len(s)-1] is 's') & (s[len(s)-2] is 'e')

    if s in unchanging_plurals_list:
        littleS = s
        return littleS
    if boolean100:
        littleS = s.replace(s[len(s)-2:], "an")
        return littleS
    if boolean1 | boolean2 | boolean4 | boolean6:
        littleS = s[:-1]
        return littleS
    if boolean3:
        littleS =  s.replace(s[len(s)-3:], "y")
        return littleS
    if boolean5:
        littleS = s[:-2]
        return littleS
    if boolean88 & boolean89:
        littleS = s[:-1]
        return littleS

    return ""


def tag_word (lx,wd):
    finalListCat = []

    for x in lx.list:
        if x[0] == wd or x[0] == verb_stem(wd) or x[0] == noun_stem(wd):
            if (x[1] == "P"):
                finalListCat.append(x[1])
            if (x[1] == "A"):
                finalListCat.append(x[1])
            if (x[1] == "N"):
                if (noun_stem(wd) == wd):
                    finalListCat.append("Ns")
                    finalListCat.append("Np")
                elif (noun_stem(wd) is ""):
                    finalListCat.append("Ns")
                else:
                    finalListCat.append("Np")
            if (x[1] == "I"):
                if (verb_stem(wd) is ""):
                    finalListCat.append("Ip")
                else:
                    finalListCat.append("Is")
            if (x[1] == "T"):
                if (verb_stem(wd) is ""):
                    finalListCat.append("Tp")
                else:
                    finalListCat.append("Ts")
    for x in function_words_tags:
        if (x[0] == wd):
            finalListCat.append(x[1])
    return finalListCat


def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

#if __name__ == "__main__":
    #lx = Lexicon()
    #lx.add("John", "P")
    #lx.add("like", "I")
    ##lx.add("fly", "I")
    #lx.add("duck", "N")
    #print noun_stem("ducks")
    #print unchanging_plurals_list
    #print lx.list
    #print tag_word(lx, "like")
    ##print verb_stem("like")
    #print verb_stem("flies")
    #print tag_word(lx, '?')
    #print tag_word(lx, "likes")
    #print tag_word(lx, "flies")

# End of PART B.
