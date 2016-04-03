"""
LogApps Challenge
TribeHacks 2016
Anna Li and Wendy Guo
"""

import nltk
import en
from nltk.data              import load
from nltk.tokenize.simple   import (SpaceTokenizer, TabTokenizer, LineTokenizer,
                                    line_tokenize)
from nltk.tokenize.regexp   import (RegexpTokenizer, WhitespaceTokenizer,
                                    BlanklineTokenizer, WordPunctTokenizer,
                                    wordpunct_tokenize, regexp_tokenize,
                                    blankline_tokenize)
from nltk.tokenize.punkt    import PunktSentenceTokenizer
from nltk.tokenize.sexpr    import SExprTokenizer, sexpr_tokenize
from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.stem.porter       import *


# Standard sentence tokenizer. Return a sentence-tokenized copy of *text*,
# using NLTK's recommended sentence tokenizer (currently :class:`.PunktSentenceTokenizer`
# for the specified language).
def sent_tokenize(text, language='english'):
    tokenizer = load('tokenizers/punkt/{0}.pickle'.format(language))
    return tokenizer.tokenize(text)


# Standard word tokenizer. Return a tokenized copy of *text*,
# using NLTK's recommended word tokenizer (currently :class:`.TreebankWordTokenizer`
# along with :class:`.PunktSentenceTokenizer`for the specified language).
_treebank_word_tokenize = TreebankWordTokenizer().tokenize
def word_tokenize(text, language="english"):
    return [token for sent in sent_tokenize(text, language) for token in _treebank_word_tokenize(sent)]


# Function that catagorizes words in a sentence by their parts of speech and and adds the words
# to their respective verb, noun, or remaining list
def categorize_words(sentence):
    word_list = word_tokenize(sentence)
    tuple_list = nltk.pos_tag(word_list)
    verbs_list = []
    real_verbs_list = []
    noun_list = []
    rem_list = []
    master_list = []
    verbstring = "VBVBDVBGVBZVBNVBP"
    nounstring = "NNNNSNNPNNPS"
    stemmer = nltk.PorterStemmer()

    for pair in tuple_list:
        if pair[1] in verbstring:
            verbs_list.append(pair[0])
        elif len(noun_list) == 0:
            if pair[1] in nounstring:
                noun_list.append(pair[0])
        else:
            rem_list.append(pair[0])

    master_list.append(noun_list)
    master_list.append(verbs_list)
    master_list.append(rem_list)

    return master_list	    


# Function for example 2 that is an expanded table to part 1
# The Global Differential GPS System sentences breakdown that includes 7 categories
def option2(verbs_list, my_csv_name):
    my_verb_dict = {}
    my_csv_file = open(my_csv_name, 'r')
    my_csv_file.readline()
    cat_strings = []
    stemmer = nltk.PorterStemmer()

    for line in my_csv_file:
        line_list = line.split(",")
        line_list[-1] = line_list[-1].rstrip()
        key_word = line_list.pop(0).lower()
        for verb in verbs_list:
            new_verb = stemmer.stem(verb)
            if new_verb in key_word:
                my_verb_dict[key_word] = line_list
            else:
                continue

    # in the end, a dictionary of verb keys and their category values are the 
    # values 
    cat_strings = ["","","","","","",""]

    for count in range(0,7):
        categories = []
        cat_sum = 0
        for key_verb in my_verb_dict:
            cat_sum += int(my_verb_dict[key_verb][count])
            categories.append(my_verb_dict[key_verb][count])
        cat_strings[count] = " + ".join(categories)
        cat_strings[count] += " = " + str(cat_sum)

    return cat_strings

 
"""
Main driver
"""

option_2 = 1
table_2 = open('table2.csv', "w")
table_2.write("Para. #,Sent. #,Subject,Verbs,Remaining\n ")

if (option_2):
    table_3 = open('table3.csv', "w")
    table_3.write("Para. #,Sent. #,Subject,Verbs,Remaining, ")
    table_3.write("Category 1, Category 2, Category 3, Category 4, Category 5, Category 6, Category 7 \n")

my_file = open("appendix1.txt", "r")
full_text = ""

for line in my_file:
    full_text += line

# split the text into paragraphs
p_list = blankline_tokenize(full_text)
p_ct = 0
for paragraph in p_list:
    newparagraph = ""
    sentence_list = paragraph.split("\t")

    trash = sentence_list.pop(0)
    if(p_ct == 1):
        trash_list = trash.split("\n")
        moretrash = trash_list.pop(0)
        for trash in trash_list:
            newparagraph += trash
    for sent in sentence_list:
        new_line_list = sent.split("\n")
        if (len(new_line_list) != 1):
            sent = new_line_list[0]
            newparagraph += " "
            if "." not in sent:
                sent += "."
            newparagraph += sent

    # split paragraphs into sentences 
    sentence_list = sent_tokenize(newparagraph)
    s_ct = 0
    for sentence in sentence_list:
        noun = ""
        verb = ""
        rem = ""
        s_ct += 1
        master_category = categorize_words(sentence)
        table_2.write(str(p_ct)+",")
        table_2.write(str(s_ct)+",")
        
        for i in master_category[0]:
            noun = noun + i + " "
        table_2.write(noun+",")
        for j in master_category[1]:
            verb = verb + j + " "
        table_2.write(verb+',')
        for l in master_category[2]:
            rem = rem + l + " "
            rem = rem.replace(',', '')
            rem = rem.replace('.', '')
             
        table_2.write(rem + "\n")
        table_3.write(str(p_ct)+",")
        table_3.write(str(s_ct)+",")
        table_3.write(noun+",")
        table_3.write(verb+",")
        table_3.write(rem+",")

        cat_strings = option2(master_category[1], 'table1.csv')
        for expr in cat_strings:
            table_3.write(expr + ", ")

        table_3.write("\n")
    p_ct += 1
   
table_3.close()   
table_2.close()







