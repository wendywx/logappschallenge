#CURRENTLY DOESN'T INCLUDE 1ST PARGARAPH 
# AND THE BERBS DON'T REALLY WORK 


import nltk
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
    tuple_list = nltk.pos_tag(word_list)
    verbs_list = []
    noun_list = []
    rem_list = []
    verbstring = "VBVBDVBGVBZVBNVBP"
    nounstring = "NNNNSNNPNNPS"

    for pair in tuple_list:
        #print(pair)

        if pair[1] in verbstring:
            verbs_list.append(pair[0])
        elif len(noun_list) == 0:
            if pair[1] in nounstring:
                noun_list.append(pair[0])
        else:
            rem_list.append(pair[0])
	    
    #print(verbs_list)
    #print(noun_list)
    #print(rem_list)
    
           
 
"""Main""" 
#nltk.download()
my_file = open("appendix1.txt", "r")
full_text = ""

for line in my_file:
    full_text += line

p_list = blankline_tokenize(full_text)
#print(p_list)

p_ct = 0
for paragraph in p_list:

    p_ct += 1
    newparagraph = ""
    sentence_list = paragraph.split("\t")

    #print sentence_list
    #print(sentence_list)
    # get rid of first x characters until a new line is hit 
    trash = sentence_list.pop(0)

    

    for sent in sentence_list:
        new_line_list = sent.split("\n")

        if (len(new_line_list) != 1):
            sent = new_line_list[0]
            newparagraph += sent

    #now we need to get rid of the characters before a tab 
    #print(newparagraph)

    sentence_list = sent_tokenize(newparagraph)
    #print(sentence_list)
    s_ct = 0
    #print sentence_list
    for sentence in sentence_list:
      
        s_ct += 1
        categorize_words(sentence)
	#print("%d",s_ct)
