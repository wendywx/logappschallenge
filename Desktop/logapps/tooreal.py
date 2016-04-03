
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
from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.tokenize.casual   import (TweetTokenizer, casual_tokenize)
from nltk.tokenize.mwe      import MWETokenizer
from nltk.tokenize.util     import string_span_tokenize, regexp_span_tokenize
from nltk.stem.porter import *


# Standard sentence tokenizer.
def sent_tokenize(text, language='english'):
    """
    Return a sentence-tokenized copy of *text*,
    using NLTK's recommended sentence tokenizer
    (currently :class:`.PunktSentenceTokenizer`
    for the specified language).
    :param text: text to split into sentences
    :param language: the model name in the Punkt corpus
    """
    tokenizer = load('tokenizers/punkt/{0}.pickle'.format(language))
    return tokenizer.tokenize(text)

# Standard word tokenizer.

_treebank_word_tokenize = TreebankWordTokenizer().tokenize
def word_tokenize(text, language="english"):
    """
    Return a tokenized copy of *text*,
    using NLTK's recommended word tokenizer
    (currently :class:`.TreebankWordTokenizer`
    along with :class:`.PunktSentenceTokenizer`
    for the specified language).

    :param text: text to split into sentences
    :param language: the model name in the Punkt corpus
    """
    return [token for sent in sent_tokenize(text, language) for token in _treebank_word_tokenize(sent)]

# finds all the verbs in a sentence 
def categorize_words(sentence):
    word_list = word_tokenize(sentence)
    
    #print("\n")
    #count = 0
    
    # for check in word_list:
    #     if "." in check:
    #         smushed_word = word_list.pop(count)
    #         smushed_list = smushed_word.split(".")
    #         word_list.append(smushed_list[0])
    #         word_list.append(smushed_list[1])
    #     count += 1

    #print(word_list)

    tuple_list = nltk.pos_tag(word_list)

    verbs_list = []
    real_verbs_list = []
    noun_list = []
    rem_list = []
    master_list = []
    verbstring = "VBVBDVBGVBZVBNVBP"
    nounstring = "NNNNSNNPNNPS"

    for pair in tuple_list:
        #print(pair)

        if pair[1] in verbstring:
            present = en.verb.present(pair[1])
            print(present)
            verbs_list.append(pair[0])

            #if pair[1] == en.verb.present(pair[1]):
               # real_verbs_list.append(pair[0])
        elif len(noun_list) == 0:
            if pair[1] in nounstring:
                noun_list.append(pair[0])
        else:
            rem_list.append(pair[0])
    
    # for verb in verbs_list:
    #     if verb == en.verb.present(verb):
    #         real_verbs_list.append(verb)

    master_list.append(noun_list)
    master_list.append(verbs_list)
    #master_list.append(real_verbs_list)
    master_list.append(rem_list)

    return master_list
	    

def option2(verbs_list, my_csv_name):
    my_verb_dict = {}
    my_csv_file = open(my_csv_name, 'r')
    my_csv_file.readline()
    cat_strings = []
#    stemmer = nltk.PorterStemmer()

    for line in my_csv_file:
        line_list = line.split(",")
        line_list[-1] = line_list[-1].rstrip()
        key_word = line_list.pop(0).lower()
        for verb in verbs_list:
            new_verb = en.verb.present(str(verb))
#            new_verb = stemmer.stem(verb)
            #print(key_word, new_verb)

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


 
"""Main""" 
#option = int(input("Which part of the problem would you like to solve? Enter 1 or 2. "))
option_2 = 1
table_2 = open('table2.csv', "w")
table_2.write("Para. #,Sent. #,Subject,Verbs,Actual Verbs,Remaining\n ")

if (option_2):
    table_3 = open('table3.csv', "w")
    table_3.write("Para. #,Sent. #,Subject,Verbs,Actual Verbs,Remaining, ")
    table_3.write("Category 1, Category 2, Category 3, Category 4, Category 5, Category 6, Category 7 \n")

my_file = open("appendix1.txt", "r")
full_text = ""

for line in my_file:
    full_text += line

p_list = blankline_tokenize(full_text)
#print(p_list)

p_ct = 0
for paragraph in p_list:
    
    newparagraph = ""
    sentence_list = paragraph.split("\t")

    #print sentence_list
    #print(sentence_list)
    # get rid of first x characters until a new line is hit

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

    #now we need to get rid of the characters before a tab 

    sentence_list = sent_tokenize(newparagraph)
    #print(sentence_list)
    s_ct = 0
    #print sentence_list
    for sentence in sentence_list:
        noun = ""
        verb = ""
        real_verb = ""
        rem = ""
        s_ct += 1
        master_category = categorize_words(sentence)
        #print(master_category)
        #print("\n")
        table_2.write(str(p_ct)+",")
        table_2.write(str(s_ct)+",")
        for i in master_category[0]:
            noun = noun + i + " "
        table_2.write(noun+",")
        for j in master_category[1]:
            verb = verb + j + " "
        table_2.write(verb+',')
        # for k in master_category[2]:
        #     real_verb = real_verb + k + " "
        # table_2.write(real_verb+',')
        for l in master_category[2]:
            rem = rem + l + " "
            rem = rem.replace(',', '')
        #print(rem)                
        table_2.write(rem + "\n")

        #if(option_2):
            
       # print (p_ct)
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
   

#if(option_2):
table_3.close()   
table_2.close()







