'''
Utilities for text preprocessing
'''
import stemmer
import re

def remove_tags (text):
    reg = re.compile('<[ \]/:a-z]*>')
    text, occ = re.subn(reg, '', text)
    return text


def remove_punc (text):
    chars = '.,:;[]()_*\'\"<>{}=-+/\\_!|^&%#'
    for c in chars:
        if c in text:
            text = text.replace(c, '')
    return text
   

def read_sw_file (fn):
    f = open(fn, 'r')
    l = f.readlines()
    f.close()
    l = map(str.strip, l)
    return l


def remove_stopw (lst):
    sw = read_sw_file('stopw.txt')
    for w in lst:
        if w in sw:
            lst.remove(w)
    

def stemming (lst):    
    ps = stemmer.PorterStemmer()
    res = []
    for w in lst:
        w = str(w)
        res.append(ps.stem(w, 0, len(w) - 1))
    return res


def preprocess (text):
    text = text.lower()
    text = remove_tags(text)
    text = remove_punc(text)
    lst = text.split()
    remove_stopw(lst)
    lst = stemming(lst)
    return lst

