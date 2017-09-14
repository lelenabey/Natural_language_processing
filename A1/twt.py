
import re
import NLPlib
from HTMLParser import HTMLParser

import sys

raw = sys.argv[1]
tokenized = sys.argv[2]
#raw = 'A1/tweets/rihanna'
#tokenized = 'A1/tokenized/rihanna.twt'

abbr_file = open('A1/abbrev.english')
pn_abbr_file = open('A1/pn_abbrev.english')
raw_tweets = open(raw, 'r')
output = open(tokenized, 'w+')
abbr = (' '.join(abbr_file.readlines())).strip().split()
pn_abbr = (' '.join(pn_abbr_file.readlines())).strip().split()
line = raw_tweets.readline()
tagger = NLPlib.NLPlib()

def html_strip_replace(line):
    line = re.sub(r'<.*?>', '', line)
    pars = HTMLParser()
    line = pars.unescape(line)
    return line

def remove_hash_at(tokens):
    for i,token in enumerate(tokens):
        tokens[i] = re.sub('[#@]', '', token)
    return tokens

def remove_urls(tokens):
    for i,token in enumerate(tokens):
        if re.search(r"(https?://)?(www.)?[a-z0-9A-Z][.][a-z0-9]+/?[a-z0-9A-Z]+?", token):
            tokens[i] = ''
    return tokens

def clitsplit(tokens):
    clitic = re.compile(r"(n't)")
    contrac = re.compile(r"('[a-z]+)")
    posses = re.compile(r"('$)")
    clitsplit=[]
    for i,token in enumerate(tokens):
        if len(clitic.split(token)) > 1:
            clitsplit+= clitic.split(token)
        elif len(contrac.split(token)) > 1:
            clitsplit+= contrac.split(token)
        else:
            clitsplit+= posses.split(token)
    return clitsplit

def split_punctuation(tokens):
    multpunc=[]
    mult = re.compile(r"([\";:,!?\(\)\-]+|[\.][\.]+)")
    for i,token in enumerate(tokens):
        #print (token)
        multpunc+= mult.split(token)
    return multpunc

def split_sentences(tokens):
    sentences =[[]]
    start = 0
    period = re.compile(r"([a-z0-9A-Z]+)([.])$")
    for i,token in enumerate(tokens):
        #print (token)
        if re.search('[.!?]$', token):
            if (token not in abbr) and (token not in pn_abbr):
                sentences += [tokens[start:i]+period.split(token)]
                start =i+1
    sentences += [tokens[start:]]
    return sentences
    
while line:    
    tokens = html_strip_replace(line).strip().split()
    tokens = remove_hash_at(tokens)
    tokens = remove_urls(tokens)
    tokens = clitsplit(tokens)
    tokens = split_punctuation(tokens)
    sentences = split_sentences(tokens)
       
        

    for s,sentence in enumerate(sentences):
        #print(' '.join(sentence))
        while '' in sentence:
            sentence.remove('')
        if len(sentence) > 0:
            tags = tagger.tag(sentence)
            #print (sentence)
            #print (tags)
        for i,word in enumerate(sentence):
            sentence[i]+='/'+tags[i]
        output.write( ' '.join(sentence)+'\n')
    output.write('|\n')
    
    line = raw_tweets.readline()

abbr_file.close()
pn_abbr_file.close()
raw_tweets.close()
output.close()
#if __name__ == "__main__":
    
