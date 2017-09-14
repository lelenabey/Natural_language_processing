import re
import sys

output = sys.argv[-1]
output_file = open(output,'w+')
output_file.write("@RELATION " + output.split(".arff")[0]+"\n\n")

features = ['First person pronouns','Second person pronouns',
'Third person pronouns','Coordinating conjunctions',
'Past-tense verbs','Future-tense verbs','Commas',
'Colons and semi-colons','Dashes','Parentheses','Ellipses',
'Common nouns','Proper nouns','Adverbs','wh-words',
'Modern slang acroynms','Words all in upper case',
'Average length of sentences','Average length of tokens',
'Number of sentences']
for feature in features:
    output_file.write('@ATTRIBUTE "' + feature + '" NUMERIC\n')
output_file.write('@ATTRIBUTE "' + "class" + '" STRING\n\n')
output_file.write('@DATA\n')
num_tweets = 9999
arg = 1
if sys.argv[arg][0] == "-":
    try:
        num_tweets = int(sys.argv[1][1:])
        arg = 2
    except:
        print("invalid arguments")




slang = ['smh', 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf', 'bff', 'wyd', 'lylc', 'brb', 'atm', 'imao', 'sml', 'btw',
'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl', 'imo', 'ltr', 'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr',
'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym', 'ur', 'u', 'sol']
slang_reg = "(" + ")|(".join(slang) + ")"
#print slang_reg



def write_dataline(feat, clss):
    output_file.write(','.join(str(x) for x in feat.values())+','+clss+'\n')
    #output.write()

def count_features(twt, num, clss):
    x=0
    line = twt.readline()
    while line and x<num:
        if x==0:
            feat = {'FPP':0, 'SPP':0, 'TPP':0, 'CC':0, 'VBD':0, 'FTV':0, 
                'COM':0, 'COL':0, 'DASH':0, 'PAR':0, 'ELIP':0, 'CNUN':0,
                'PNUN':0, 'ADV':0, 'WHW':0, 'SLNG':0, 'CAPS':0, 'ALS':0, 
                'ALT':0, 'NOS':0}
        if '|' not in line:
            x+=1
            tokens = line.strip().split()
            for i,token in enumerate(tokens):
                if re.search(r"/PRP",token):
                    if re.search('i|me|my|mine|we|us|our|ours', token, re.IGNORECASE):
                        feat['FPP']+=1
                    elif re.search('you|your|yours|u|ur|urs', token, re.IGNORECASE):
                        feat['SPP']+=1
                    elif re.search('he|him|his|she|her|hers|it|its|they|them|their|theirs', token, re.IGNORECASE):
                        feat['TPP']+=1
                if re.search(r"/CC",token):
                    feat['CC']+=1
                if re.search(r"/VBD",token):
                    feat['VBD']+=1
                if re.search(r"/MD|/VBG", token):
                    if re.search(r"'ll|will|gonna", token, re.IGNORECASE):
                        feat['FTV']+=1
                if re.search('going', token, re.IGNORECASE):
                    try :
                        if re.search(r"/TO", tokens[i+1]) and re.search(r"/VB", tokens[i+2]):
                            feat['FTV']+=1
                    except IndexError:
                        pass
                if re.search(r",/,", token):
                    feat['COM']+=1
                if re.search(r":|;", token):
                    feat['COL']+=1
                if re.search(r"-/:", token):
                    feat['DASH']+=1
                if re.search(r"\(|\)", token):
                    feat['PAR']+=1
                if re.search(r"[.][.]+", token):
                    feat['ELIP']+=1
                if re.search(r"/NN|/NNS", token):
                    feat['CNUN']+=1
                if re.search(r"/NNP|/NNPS", token):
                    feat['PNUN']+=1
                if re.search(r"/RB|/RBR|/RBS", token):
                    feat['ADV']+=1
                if re.search(r"/WDT|/WP|/WP\$|/WRB", token):
                    feat['WHW']+=1
                if re.sub('/[A-Z]+', '', token).lower() in slang:
                    feat['SLNG']+=1
                if re.match('[A-Z][A-Z]+/[A-z]+',token):
                    feat['CAPS']+=1
                if re.match('\W', token):
                    feat['ALT']+=len(token)
            feat['ALS']+=len(tokens)
            feat['NOS']+=1

        else:
            if feat['ALS'] > 0:
                feat['ALT']= feat['ALT']/feat['ALS']
            if feat['NOS']>0:
                feat['ALS']= feat['ALS']/feat['NOS']
            write_dataline(feat, clss)
            feat = {'FPP':0, 'SPP':0, 'TPP':0, 'CC':0, 'VBD':0, 'FTV':0, 
                'COM':0, 'COL':0, 'DASH':0, 'PAR':0, 'ELIP':0, 'CNUN':0,
                'PNUN':0, 'ADV':0, 'WHW':0, 'SLNG':0, 'CAPS':0, 'ALS':0, 
                'ALT':0, 'NOS':0}
        
        line = twt.readline()
    #print tokens

def count_class(clss, file_list):
    for twt in file_list:
        current_file = open(twt, 'r')
        count_features(current_file, num_tweets, clss)


for files in sys.argv[arg:-1]:
    if ":" in files:
        clss = files.split(":")[0]
        file_list = files.split(':')[1].split('+')
    else:
        file_list = files.split('+')
        clss = re.sub(r"[\.]twt|\+", '', files)
    count_class(clss, file_list)